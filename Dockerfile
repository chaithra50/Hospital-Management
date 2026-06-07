FROM eclipse-temurin:17-jdk-alpine

WORKDIR /app

COPY target/hms-1.0.0.jar hms-app.jar

EXPOSE 8080

ENV SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/hospital_management_system
ENV SPRING_DATASOURCE_USERNAME=hms_user
ENV SPRING_DATASOURCE_PASSWORD=hms_password
ENV JWT_SECRET=mySecretKeyForJWTTokenSigningThatIsLongEnoughFor512BitHS512Algorithm2024
ENV JWT_EXPIRATION=86400000

ENTRYPOINT ["java", "-jar", "hms-app.jar"]
