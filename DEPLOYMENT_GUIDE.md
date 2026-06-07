# Hospital Management System - Deployment Guide

Production deployment guide for HMS REST API across different platforms.

---

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Azure Deployment](#azure-deployment)
5. [Production Configuration](#production-configuration)
6. [Database Backup & Recovery](#database-backup--recovery)
7. [Monitoring & Logging](#monitoring--logging)
8. [Security Hardening](#security-hardening)

---

## Local Development

### Environment Variables
```bash
# Create .env file
export SPRING_DATASOURCE_URL=jdbc:mysql://localhost:3306/hospital_management_system
export SPRING_DATASOURCE_USERNAME=hms_user
export SPRING_DATASOURCE_PASSWORD=hms_password
export JWT_SECRET=MyVerySecureJWTSecret2024WithHighSecurity
export JWT_EXPIRATION=86400000
export SERVER_PORT=8080
```

### Run with profiles
```bash
mvn spring-boot:run -Dspring-boot.run.arguments="--spring.profiles.active=dev"
```

---

## Docker Deployment

### 1. Build Docker Image

Create `Dockerfile`:
```dockerfile
FROM openjdk:17-jdk-slim

# Set working directory
WORKDIR /app

# Copy JAR file
COPY target/hospital-management-system-1.0.0.jar hms-app.jar

# Expose port
EXPOSE 8080

# Environment variables
ENV SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/hospital_management_system
ENV SPRING_DATASOURCE_USERNAME=hms_user
ENV SPRING_DATASOURCE_PASSWORD=hms_password
ENV JWT_SECRET=ProductionJWTSecret2024
ENV JWT_EXPIRATION=86400000

# Run application
ENTRYPOINT ["java", "-jar", "hms-app.jar"]
```

### 2. Build Image
```bash
mvn clean package
docker build -t hospital-management-system:1.0.0 .
docker build -t hospital-management-system:latest .
```

### 3. Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: hms-mysql
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: hospital_management_system
      MYSQL_USER: hms_user
      MYSQL_PASSWORD: hms_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./src/main/resources/db/migration:/docker-entrypoint-initdb.d
    networks:
      - hms-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  app:
    image: hospital-management-system:latest
    container_name: hms-app
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/hospital_management_system?createDatabaseIfNotExist=true
      SPRING_DATASOURCE_USERNAME: hms_user
      SPRING_DATASOURCE_PASSWORD: hms_password
      JWT_SECRET: ProductionJWTSecret2024
      JWT_EXPIRATION: 86400000
      SERVER_PORT: 8080
    ports:
      - "8080:8080"
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - hms-network
    restart: unless-stopped

  nginx:
    image: nginx:latest
    container_name: hms-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - hms-network

volumes:
  mysql_data:

networks:
  hms-network:
    driver: bridge
```

### 4. Run Docker Compose
```bash
docker-compose up -d
docker-compose logs -f app
docker-compose ps
docker-compose down
```

---

## AWS Deployment

### 1. Using AWS RDS for MySQL

```bash
# Create RDS instance
aws rds create-db-instance \
  --db-instance-identifier hms-mysql \
  --db-instance-class db.t3.micro \
  --engine mysql \
  --engine-version 8.0.28 \
  --master-username hms_user \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20
```

### 2. Push to ECR (Elastic Container Registry)

```bash
# Create ECR repository
aws ecr create-repository --repository-name hospital-management-system

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

# Tag image
docker tag hospital-management-system:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/hospital-management-system:latest

# Push image
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/hospital-management-system:latest
```

### 3. Deploy on ECS (Elastic Container Service)

Create `ecs-task-definition.json`:
```json
{
  "family": "hms-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "hms-app",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/hospital-management-system:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "hostPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "SPRING_DATASOURCE_URL",
          "value": "jdbc:mysql://rds-endpoint:3306/hospital_management_system"
        },
        {
          "name": "SPRING_DATASOURCE_USERNAME",
          "value": "hms_user"
        },
        {
          "name": "JWT_SECRET",
          "value": "ProductionSecret2024"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/hms-app",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Register and deploy:
```bash
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json
aws ecs create-service --cluster hms-cluster --service-name hms-service --task-definition hms-task:1 --desired-count 2
```

### 4. Setup ALB (Application Load Balancer)

```bash
aws elbv2 create-load-balancer \
  --name hms-alb \
  --subnets subnet-12345678 subnet-87654321

aws elbv2 create-target-group \
  --name hms-targets \
  --protocol HTTP \
  --port 8080 \
  --vpc-id vpc-12345678
```

---

## Azure Deployment

### 1. Create App Service

```bash
# Create resource group
az group create --name hms-rg --location eastus

# Create App Service plan
az appservice plan create \
  --name hms-plan \
  --resource-group hms-rg \
  --sku B2 --is-linux

# Create webapp
az webapp create \
  --resource-group hms-rg \
  --plan hms-plan \
  --name hospital-management-system \
  --runtime "JAVA|17-java17"
```

### 2. Configure Environment Variables

```bash
az webapp config appsettings set \
  --resource-group hms-rg \
  --name hospital-management-system \
  --settings \
    SPRING_DATASOURCE_URL=jdbc:mysql://host:3306/hospital_management_system \
    SPRING_DATASOURCE_USERNAME=hms_user \
    SPRING_DATASOURCE_PASSWORD=hms_password \
    JWT_SECRET=ProductionSecret2024 \
    WEBSITES_PORT=8080
```

### 3. Deploy JAR

```bash
az webapp deployment source config-zip \
  --resource-group hms-rg \
  --name hospital-management-system \
  --src hospital-management-system-1.0.0.jar
```

### 4. Setup Azure Database for MySQL

```bash
az mysql server create \
  --resource-group hms-rg \
  --name hms-mysql-server \
  --location eastus \
  --admin-user hms_user \
  --admin-password YOUR_PASSWORD \
  --sku-name B_Gen5_1
```

---

## Production Configuration

### 1. Production Properties

Create `application-prod.properties`:
```properties
# Server
server.port=8080
server.servlet.context-path=/api
server.compression.enabled=true
server.compression.min-response-size=1024

# Database
spring.datasource.url=${SPRING_DATASOURCE_URL}
spring.datasource.username=${SPRING_DATASOURCE_USERNAME}
spring.datasource.password=${SPRING_DATASOURCE_PASSWORD}
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.MySQL8Dialect

# JWT
jwt.secret=${JWT_SECRET}
jwt.expiration=${JWT_EXPIRATION}

# Logging
logging.level.root=INFO
logging.level.com.hms=INFO
logging.file.name=/var/log/hms/application.log
logging.file.max-size=10MB
logging.file.max-history=10

# Actuator
management.endpoints.web.exposure.include=health,metrics
management.endpoint.health.show-details=when-authorized
```

### 2. SSL/TLS Configuration

```properties
# SSL Configuration
server.ssl.enabled=true
server.ssl.key-store=${SSL_KEYSTORE_PATH}
server.ssl.key-store-password=${SSL_KEYSTORE_PASSWORD}
server.ssl.key-store-type=PKCS12
server.ssl.key-alias=tomcat
```

### 3. CORS Configuration

Update `SecurityConfig.java`:
```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration configuration = new CorsConfiguration();
    configuration.setAllowedOrigins(Arrays.asList("https://yourdomain.com"));
    configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    configuration.setAllowedHeaders(Arrays.asList("*"));
    configuration.setAllowCredentials(true);
    
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", configuration);
    return source;
}
```

---

## Database Backup & Recovery

### 1. MySQL Backup

```bash
# Full backup
mysqldump -u hms_user -p hospital_management_system > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup with compression
mysqldump -u hms_user -p hospital_management_system | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Scheduled backup (cron)
0 2 * * * mysqldump -u hms_user -p$PASSWORD hospital_management_system | gzip > /backups/backup_$(date +\%Y\%m\%d_\%H\%M\%S).sql.gz
```

### 2. Restore Database

```bash
# Restore from backup
mysql -u hms_user -p hospital_management_system < backup_20240522_120000.sql

# Restore from compressed backup
gunzip < backup_20240522_120000.sql.gz | mysql -u hms_user -p hospital_management_system
```

### 3. AWS RDS Backup

```bash
# Create snapshot
aws rds create-db-snapshot \
  --db-instance-identifier hms-mysql \
  --db-snapshot-identifier hms-backup-$(date +%Y%m%d)

# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier hms-mysql-restored \
  --db-snapshot-identifier hms-backup-20240522
```

---

## Monitoring & Logging

### 1. Application Metrics

Update `pom.xml`:
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

Configure `application.properties`:
```properties
management.endpoints.web.exposure.include=health,metrics,prometheus
management.metrics.export.prometheus.enabled=true
```

Access metrics:
```bash
curl http://localhost:8080/api/actuator/metrics
curl http://localhost:8080/api/actuator/prometheus
```

### 2. ELK Stack (Elasticsearch, Logstash, Kibana)

Add dependency:
```xml
<dependency>
    <groupId>co.elastic.logging</groupId>
    <artifactId>logback-ecs-encoder</artifactId>
    <version>1.3.0</version>
</dependency>
```

Create `logback-spring.xml`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <property name="LOG_FILE" value="${LOG_FILE:-${LOG_PATH:-${LOG_TEMP:-${java.io.tmpdir:-/tmp}}/}spring.log}"/>
    
    <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
        <file>${LOG_FILE}</file>
        <encoder class="co.elastic.logging.logback.EcsEncoder"/>
        <rollingPolicy class="ch.qos.logback.core.rolling.SizeAndTimeBasedRollingPolicy">
            <fileNamePattern>${LOG_FILE}.%d{yyyy-MM-dd}.%i.gz</fileNamePattern>
            <maxFileSize>10MB</maxFileSize>
            <maxHistory>30</maxHistory>
        </rollingPolicy>
    </appender>
    
    <root level="INFO">
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

### 3. Datadog Integration

```bash
# Install Datadog Agent
bash -c "$(curl -L https://s3.amazonaws.com/dd-agent/scripts/install_mac_os.sh)"

# Configure for JVM monitoring
export DD_SERVICE=hospital-management-system
export DD_TRACE_ENABLED=true
export DD_PROFILING_ENABLED=true

java -javaagent:dd-java-agent.jar -Ddd.service=$DD_SERVICE -jar hms-app.jar
```

---

## Security Hardening

### 1. WAF Rules (AWS WAF)

```bash
# Create IP whitelist rule
aws wafv2 create-ip-set \
  --name hms-whitelist \
  --scope CLOUDFRONT \
  --ip-address-version IPV4 \
  --addresses CIDR_BLOCKS
```

### 2. DDoS Protection

Enable AWS Shield Standard (automatic) or Shield Advanced:
```bash
aws shield subscribe
```

### 3. Rate Limiting

Update `SecurityConfig.java`:
```java
http.authorizeRequests()
    .requestMatchers(antMatcher("/api/auth/login")).permitAll()
    .anyRequest().authenticated()
    .and()
    .addFilterBefore(new RateLimitingFilter(10), UsernamePasswordAuthenticationFilter.class);
```

### 4. HTTPS Only

```properties
server.servlet.session.cookie.secure=true
server.servlet.session.cookie.http-only=true
server.servlet.session.cookie.same-site=strict
```

### 5. Security Headers

```java
@Configuration
public class SecurityHeadersConfig extends WebSecurityConfigurerAdapter {
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.headers()
            .contentSecurityPolicy("default-src 'self'")
            .and()
            .xssProtection()
            .and()
            .frameOptions().DENY()
            .and()
            .httpStrictTransportSecurity()
            .maxAgeInSeconds(31536000);
    }
}
```

---

## Health Check

### 1. Startup Probe
```bash
curl -f http://localhost:8080/api/actuator/health || exit 1
```

### 2. Liveness Probe
```bash
curl -f http://localhost:8080/api/actuator/health/liveness || exit 1
```

### 3. Readiness Probe
```bash
curl -f http://localhost:8080/api/actuator/health/readiness || exit 1
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Memory leaks | Use JVM profilers, analyze heap dumps |
| Database connection timeout | Increase pool size, check network |
| High CPU usage | Profile application, optimize queries |
| JWT expiration | Implement refresh token mechanism |

---

**Version:** 1.0.0  
**Last Updated:** May 2024
