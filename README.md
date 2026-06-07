# Hospital Management System (HMS) - REST API

A comprehensive, production-ready Spring Boot 3.x REST API for Hospital Management System with complete JWT authentication, role-based access control, and all essential hospital operations.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Role-Based Access Control](#role-based-access-control)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)

## 🎯 Features

### 1. **Auth Module**
- User registration and login with JWT tokens
- Role-based access control (ADMIN, DOCTOR, NURSE, RECEPTIONIST, PATIENT)
- Password encryption and validation
- User profile management
- Password change functionality
- Email and username availability check

### 2. **Patient Module**
- Patient registration and profile management
- Admission and discharge functionality
- Blood group tracking
- Medical history and allergies
- Emergency contact information
- Pagination and search capabilities

### 3. **Doctor Module**
- Doctor registration and specialization tracking
- License number validation
- Department assignment
- Availability management
- Doctor schedule management
- Search doctors by specialization or department

### 4. **Appointment Module**
- Appointment booking with slot conflict checking
- Appointment rescheduling and cancellation
- Appointment status tracking (SCHEDULED, COMPLETED, CANCELLED, etc.)
- Upcoming appointments view
- Doctor's daily appointment schedule

### 5. **Billing Module**
- Invoice generation
- Payment tracking
- Multiple payment status (PENDING, PAID, PARTIAL, CANCELLED)
- Patient invoice history
- Revenue reporting

### 6. **Medical Records Module**
- Prescription management
- Medicine details with dosage and frequency
- Patient prescription history
- Appointment-based medical records

### 7. **Inventory Module**
- Medicine stock management
- Low stock alerts (reorder level)
- Expiry date tracking
- Medicine search and filtering
- Stock updates and notifications

## 📁 Project Structure

```
Hospital Management System/
├── src/
│   ├── main/
│   │   ├── java/com/hms/
│   │   │   ├── auth/
│   │   │   │   ├── entity/
│   │   │   │   ├── dto/
│   │   │   │   ├── repository/
│   │   │   │   ├── service/
│   │   │   │   └── controller/
│   │   │   ├── patient/
│   │   │   ├── doctor/
│   │   │   ├── appointment/
│   │   │   ├── billing/
│   │   │   ├── medicalrecords/
│   │   │   ├── inventory/
│   │   │   ├── exception/
│   │   │   ├── config/
│   │   │   └── util/
│   │   └── resources/
│   │       ├── application.properties
│   │       └── db/migration/ (Flyway scripts)
│   └── test/
│       └── java/com/hms/
│           └── (Unit tests)
├── pom.xml
└── README.md
```

## 🛠 Technology Stack

- **Framework**: Spring Boot 3.2.0
- **Language**: Java 17
- **Security**: Spring Security + JWT (JSON Web Tokens)
- **Database**: MySQL 8.0
- **ORM**: Spring Data JPA & Hibernate
- **Build Tool**: Maven 3.8+
- **API Documentation**: Swagger/OpenAPI 3
- **Database Migration**: Flyway
- **Testing**: JUnit 5, Mockito
- **Logging**: SLF4J

## ✅ Prerequisites

- Java 17 or higher
- Maven 3.8 or higher
- MySQL 8.0 or higher
- Git
- IDE (IntelliJ IDEA, Eclipse, VS Code, etc.)

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd "Hospital Management"
```

### Step 2: Create MySQL Database
```sql
CREATE DATABASE hospital_management_system;
```

### Step 3: Configure Application Properties
Edit `src/main/resources/application.properties`:

```properties
# Database Configuration
spring.datasource.url=jdbc:mysql://localhost:3306/hospital_management_system?createDatabaseIfNotExist=true&useSSL=false&serverTimezone=UTC
spring.datasource.username=root
spring.datasource.password=your_password

# JWT Configuration
jwt.secret=MyVeryLongAndComplexJWTSecretKeyForHospitalManagementSystem2024
jwt.expiration=86400000

# Server Port
server.port=8080
```

### Step 4: Build the Project
```bash
mvn clean install
```

### Step 5: Run the Application
```bash
mvn spring-boot:run
```

The application will start at `http://localhost:8080`

### Step 6: Access Swagger UI
Visit: `http://localhost:8080/swagger-ui.html`

## ⚙️ Configuration

### JWT Configuration
- **Secret Key**: Configured in `application.properties`
- **Expiration Time**: 24 hours (86400000 ms)
- **Algorithm**: HS512

### Database Configuration
- **Type**: MySQL 8.0
- **Connection Pool**: HikariCP
- **Dialect**: MySQL8Dialect
- **Migration Tool**: Flyway (auto-applied on startup)

### Logging Configuration
```properties
logging.level.root=INFO
logging.level.com.hms=DEBUG
logging.level.org.springframework.security=DEBUG
```

## 🔐 Authentication

### Login
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "usernameOrEmail": "john_doe",
    "password": "SecurePassword123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzUxMiJ9...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "PATIENT",
  "message": "Login successful"
}
```

### Using Token in Requests
```bash
curl -X GET http://localhost:8080/api/patients \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

## 👥 Role-Based Access Control

| Role | Permissions |
|------|------------|
| **ADMIN** | Full access to all endpoints |
| **DOCTOR** | View/manage patients, create appointments, add prescriptions |
| **NURSE** | View patients, manage inventory, view appointments |
| **RECEPTIONIST** | Manage appointments, create invoices, patient registration |
| **PATIENT** | View own profile, book appointments, view medical records |

## 🗄️ Database Schema

### Key Tables
- `users` - System users
- `patients` - Patient information
- `doctors` - Doctor information
- `doctor_schedules` - Doctor availability
- `appointments` - Appointment records
- `invoices` - Billing invoices
- `prescriptions` - Medication prescriptions
- `medicines` - Inventory medicines
- `lab_reports` - Lab test results
- `visit_history` - Patient visit history

All migrations are handled by Flyway (`src/main/resources/db/migration/`)

## 📡 API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /profile` - Get current user profile
- `GET /profile/{userId}` - Get user profile
- `PUT /profile/{userId}` - Update profile
- `POST /change-password/{userId}` - Change password
- `GET /check-email` - Check email availability
- `GET /check-username` - Check username availability
- `POST /logout` - Logout

### Patients (`/api/patients`)
- `POST /register` - Register new patient
- `GET /{patientId}` - Get patient details
- `GET /user/{userId}` - Get patient by user ID
- `PUT /{patientId}` - Update patient profile
- `GET` - Get all patients (paginated)
- `GET /search` - Search patients
- `POST /{patientId}/admit` - Admit patient
- `POST /{patientId}/discharge` - Discharge patient
- `GET /admitted` - Get admitted patients
- `DELETE /{patientId}` - Delete patient

### Doctors (`/api/doctors`)
- `POST /register` - Register new doctor
- `GET /{doctorId}` - Get doctor profile
- `PUT /{doctorId}` - Update doctor profile
- `GET` - Get all doctors (paginated)
- `GET /search` - Search doctors
- `GET /specialization/{spec}` - Get doctors by specialization
- `GET /available` - Get available doctors
- `PUT /{doctorId}/availability` - Set availability
- `POST /{doctorId}/schedules` - Add schedule
- `GET /{doctorId}/schedules` - Get schedules
- `DELETE /schedules/{scheduleId}` - Delete schedule

### Appointments (`/api/appointments`)
- `POST` - Book appointment
- `GET /{appointmentId}` - Get appointment
- `GET /patient/{patientId}` - Get patient appointments
- `GET /doctor/{doctorId}` - Get doctor appointments
- `POST /{appointmentId}/cancel` - Cancel appointment
- `POST /{appointmentId}/reschedule` - Reschedule appointment
- `POST /{appointmentId}/complete` - Complete appointment
- `GET /upcoming` - Get upcoming appointments

### Billing (`/api/billing`)
- `POST /invoices` - Create invoice
- `GET /invoices/{invoiceId}` - Get invoice
- `GET /invoices/patient/{patientId}` - Get patient invoices
- `POST /invoices/{invoiceId}/payment` - Record payment

### Medical Records (`/api/medical-records`)
- `POST /prescriptions` - Add prescription
- `GET /prescriptions/{prescriptionId}` - Get prescription
- `GET /prescriptions/appointment/{appointmentId}` - Get appointment prescriptions
- `GET /prescriptions/patient/{patientId}` - Get patient prescriptions

### Inventory (`/api/inventory`)
- `POST /medicines` - Add medicine
- `GET /medicines/{medicineId}` - Get medicine
- `GET /medicines` - Get all medicines
- `GET /medicines/search` - Search medicines
- `PUT /medicines/{medicineId}/stock` - Update stock
- `GET /medicines/stock/low` - Get low stock items
- `GET /medicines/expired` - Get expired medicines

## 🧪 Testing

### Run All Tests
```bash
mvn test
```

### Run Specific Test Class
```bash
mvn test -Dtest=AuthServiceImplTest
```

### Run Tests with Coverage
```bash
mvn test jacoco:report
```

Test files are located in `src/test/java/com/hms/`

## 📦 Build & Deployment

### Build JAR
```bash
mvn clean package
```

### Run JAR
```bash
java -jar target/hms-1.0.0.jar
```

### Docker Support (Optional)
Create `Dockerfile`:
```dockerfile
FROM openjdk:17-jdk-slim
COPY target/hms-1.0.0.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Build and run:
```bash
docker build -t hms:latest .
docker run -p 8080:8080 --name hms hms:latest
```

## 📚 Example Workflows

### Register and Login as Patient
1. Register: `POST /api/auth/register`
2. Login: `POST /api/auth/login`
3. Get profile: `GET /api/auth/profile`

### Book Appointment
1. Get available doctors: `GET /api/doctors/available`
2. Get doctor schedules: `GET /api/doctors/{doctorId}/schedules`
3. Book appointment: `POST /api/appointments`

### Manage Patient Admission
1. Admit patient: `POST /api/patients/{patientId}/admit`
2. View admitted patients: `GET /api/patients/admitted`
3. Discharge patient: `POST /api/patients/{patientId}/discharge`

### Create and Manage Invoices
1. Create invoice: `POST /api/billing/invoices`
2. Get invoice: `GET /api/billing/invoices/{invoiceId}`
3. Record payment: `POST /api/billing/invoices/{invoiceId}/payment`

## 🐛 Error Handling

All endpoints return standardized error responses:

```json
{
  "status": 404,
  "message": "Resource not found",
  "error": "Resource Not Found",
  "timestamp": "2024-05-22T10:30:00",
  "path": "/api/patients/999",
  "fieldErrors": null
}
```

## 📝 License

This project is licensed under the Apache 2.0 License.

## 👨‍💻 Contributing

Contributions are welcome! Please follow the existing code structure and create pull requests.

## 📧 Support

For issues and questions, please open an issue in the repository.

---

**Happy coding! 🎉**
