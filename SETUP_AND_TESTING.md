# Hospital Management System - Setup & Testing Guide

Complete guide for setting up and testing the HMS REST API project.

## Quick Start

### Prerequisites
- Java 17+
- MySQL 8.0+
- Maven 3.8+
- Postman/Insomnia (optional, for testing)

### Step-by-Step Setup

#### 1. Database Setup
```sql
-- Open MySQL CLI
mysql -u root -p

-- Create database
CREATE DATABASE hospital_management_system;
CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'hms_password';
GRANT ALL PRIVILEGES ON hospital_management_system.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 2. Configure Application
Edit `src/main/resources/application.properties`:
```properties
# Database
spring.datasource.url=jdbc:mysql://localhost:3306/hospital_management_system
spring.datasource.username=hms_user
spring.datasource.password=hms_password

# JWT
jwt.secret=MyVeryLongSecretKeyForHMS2024WithHighSecurity
jwt.expiration=86400000

# Server
server.port=8080
server.servlet.context-path=/api
```

#### 3. Build Project
```bash
cd "Hospital Management"
mvn clean install
```

#### 4. Run Application
```bash
mvn spring-boot:run
```

Application starts at: `http://localhost:8080`
Swagger UI: `http://localhost:8080/swagger-ui.html`

---

## Running Tests

### Unit Tests

Run all tests:
```bash
mvn test
```

Run specific test class:
```bash
mvn test -Dtest=AuthServiceImplTest
mvn test -Dtest=PatientServiceImplTest
mvn test -Dtest=DoctorServiceImplTest
mvn test -Dtest=AppointmentServiceImplTest
mvn test -Dtest=BillingServiceImplTest
mvn test -Dtest=MedicalRecordsServiceImplTest
mvn test -Dtest=InventoryServiceImplTest
```

Run tests with code coverage:
```bash
mvn clean test jacoco:report
# Report: target/site/jacoco/index.html
```

Skip tests during build:
```bash
mvn clean install -DskipTests
```

---

## API Testing Workflow

### 1. Authentication Flow

#### a) Register as PATIENT
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "patient_john",
    "email": "patient@example.com",
    "password": "PatientPass123!",
    "firstName": "John",
    "lastName": "Patient",
    "phoneNumber": "9876543210",
    "role": "PATIENT"
  }'
```

Save the `access_token` from response as `$PATIENT_TOKEN`

#### b) Register as DOCTOR
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "doctor_james",
    "email": "doctor@example.com",
    "password": "DoctorPass123!",
    "firstName": "Dr. James",
    "lastName": "Wilson",
    "phoneNumber": "9876543211",
    "role": "DOCTOR"
  }'
```

Save the `access_token` as `$DOCTOR_TOKEN`

#### c) Register as ADMIN
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin_user",
    "email": "admin@example.com",
    "password": "AdminPass123!",
    "firstName": "Admin",
    "lastName": "User",
    "phoneNumber": "9876543212",
    "role": "ADMIN"
  }'
```

Save the `access_token` as `$ADMIN_TOKEN`

---

### 2. Patient Module Testing

#### Register Patient
```bash
curl -X POST http://localhost:8080/api/patients/register \
  -H "Authorization: Bearer $PATIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "John",
    "lastName": "Patient",
    "email": "patient@example.com",
    "phoneNumber": "9876543210",
    "bloodGroup": "O+",
    "gender": "MALE",
    "dateOfBirth": "1990-05-15",
    "allergies": "Penicillin",
    "medicalConditions": "None",
    "emergencyContactName": "Jane Patient",
    "emergencyContactPhone": "9876543213"
  }'
```

Save returned `id` as `$PATIENT_ID`

#### Get Patient by ID
```bash
curl -X GET http://localhost:8080/api/patients/$PATIENT_ID \
  -H "Authorization: Bearer $PATIENT_TOKEN"
```

#### Admit Patient (as ADMIN)
```bash
curl -X POST http://localhost:8080/api/patients/$PATIENT_ID/admit \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "wardNumber": "101",
    "bedNumber": "5",
    "reasonForAdmission": "Acute Bronchitis",
    "expectedDischargeDate": "2024-06-15"
  }'
```

#### Get All Admitted Patients
```bash
curl -X GET "http://localhost:8080/api/patients/admitted?page=0&size=20" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

### 3. Doctor Module Testing

#### Register Doctor (as ADMIN)
```bash
curl -X POST http://localhost:8080/api/doctors/register \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Dr. James",
    "lastName": "Wilson",
    "email": "doctor@example.com",
    "phoneNumber": "9876543211",
    "specialization": "Cardiology",
    "licenseNumber": "LIC123456",
    "yearsOfExperience": 15,
    "department": "Cardiology",
    "consultationFee": 500.00
  }'
```

Save returned `id` as `$DOCTOR_ID`

#### Get Available Doctors
```bash
curl -X GET http://localhost:8080/api/doctors/available \
  -H "Authorization: Bearer $PATIENT_TOKEN"
```

#### Get Doctors by Specialization
```bash
curl -X GET http://localhost:8080/api/doctors/specialization/Cardiology \
  -H "Authorization: Bearer $PATIENT_TOKEN"
```

#### Add Doctor Schedule
```bash
curl -X POST http://localhost:8080/api/doctors/$DOCTOR_ID/schedules \
  -H "Authorization: Bearer $DOCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "doctorId": '$DOCTOR_ID',
    "dayOfWeek": "MONDAY",
    "startTime": "09:00",
    "endTime": "17:00",
    "slotDurationMinutes": 30
  }'
```

---

### 4. Appointment Module Testing

#### Book Appointment
```bash
curl -X POST http://localhost:8080/api/appointments \
  -H "Authorization: Bearer $PATIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": '$PATIENT_ID',
    "doctorId": '$DOCTOR_ID',
    "appointmentDate": "2024-06-20T14:30:00",
    "reasonForVisit": "Regular Checkup",
    "notes": "Patient has hypertension history"
  }'
```

Save returned `id` as `$APPOINTMENT_ID`

#### Get Appointment Details
```bash
curl -X GET http://localhost:8080/api/appointments/$APPOINTMENT_ID \
  -H "Authorization: Bearer $PATIENT_TOKEN"
```

#### Complete Appointment (as DOCTOR)
```bash
curl -X POST http://localhost:8080/api/appointments/$APPOINTMENT_ID/complete \
  -H "Authorization: Bearer $DOCTOR_TOKEN"
```

#### Get Patient Appointments
```bash
curl -X GET "http://localhost:8080/api/appointments/patient/$PATIENT_ID?page=0&size=20" \
  -H "Authorization: Bearer $PATIENT_TOKEN"
```

---

### 5. Billing Module Testing

#### Create Invoice
```bash
curl -X POST "http://localhost:8080/api/billing/invoices?appointmentId=$APPOINTMENT_ID&amount=5000.00" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

Save returned `id` as `$INVOICE_ID`

#### Record Payment
```bash
curl -X POST "http://localhost:8080/api/billing/invoices/$INVOICE_ID/payment?amount=2500.00" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

#### Get Patient Invoices
```bash
curl -X GET "http://localhost:8080/api/billing/invoices/patient/$PATIENT_ID?page=0&size=20" \
  -H "Authorization: Bearer $PATIENT_TOKEN"
```

---

### 6. Medical Records Module Testing

#### Add Prescription (as DOCTOR)
```bash
curl -X POST http://localhost:8080/api/medical-records/prescriptions \
  -H "Authorization: Bearer $DOCTOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "appointmentId": '$APPOINTMENT_ID',
    "medicineName": "Aspirin",
    "dosage": "500mg",
    "frequency": "Twice daily",
    "durationDays": 7,
    "quantity": 14,
    "instructions": "Take with food"
  }'
```

#### Get Patient Prescriptions
```bash
curl -X GET http://localhost:8080/api/medical-records/prescriptions/patient/$PATIENT_ID \
  -H "Authorization: Bearer $PATIENT_TOKEN"
```

---

### 7. Inventory Module Testing

#### Add Medicine (as ADMIN)
```bash
curl -X POST http://localhost:8080/api/inventory/medicines \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Aspirin",
    "description": "Pain reliever and anti-inflammatory",
    "manufacturer": "PharmaCorp",
    "unitPrice": 50.00,
    "quantityInStock": 100,
    "reorderLevel": 20,
    "expiryDate": "2026-05-22"
  }'
```

Save returned `id` as `$MEDICINE_ID`

#### Update Medicine Stock
```bash
curl -X PUT "http://localhost:8080/api/inventory/medicines/$MEDICINE_ID/stock?quantity=50" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

#### Get Low Stock Medicines
```bash
curl -X GET http://localhost:8080/api/inventory/medicines/stock/low \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

#### Search Medicines
```bash
curl -X GET "http://localhost:8080/api/inventory/medicines/search?name=Aspirin&page=0&size=20" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

## Automated Testing Script

Create `test.sh`:
```bash
#!/bin/bash

BASE_URL="http://localhost:8080/api"

echo "=== HMS REST API Testing ==="

# Register and login
echo -e "\n1. Testing Authentication..."
PATIENT_RESPONSE=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_patient",
    "email": "test@example.com",
    "password": "TestPass123!",
    "firstName": "Test",
    "lastName": "Patient",
    "phoneNumber": "9876543210",
    "role": "PATIENT"
  }')

PATIENT_TOKEN=$(echo $PATIENT_RESPONSE | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
echo "✓ Patient registered and logged in"

# Get profile
echo -e "\n2. Testing Patient Profile..."
curl -s -X GET $BASE_URL/auth/profile \
  -H "Authorization: Bearer $PATIENT_TOKEN" | jq '.'
echo "✓ Profile retrieved"

# Register patient
echo -e "\n3. Testing Patient Registration..."
PATIENT_REG=$(curl -s -X POST $BASE_URL/patients/register \
  -H "Authorization: Bearer $PATIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Test",
    "lastName": "Patient",
    "email": "test@example.com",
    "phoneNumber": "9876543210",
    "bloodGroup": "O+",
    "gender": "MALE",
    "dateOfBirth": "1990-05-15",
    "allergies": "None",
    "medicalConditions": "None",
    "emergencyContactName": "Test Contact",
    "emergencyContactPhone": "9876543211"
  }')

PATIENT_ID=$(echo $PATIENT_REG | grep -o '"id":[0-9]*' | cut -d':' -f2 | head -1)
echo "✓ Patient registered with ID: $PATIENT_ID"

echo -e "\n=== All tests completed ==="
```

Run tests:
```bash
chmod +x test.sh
./test.sh
```

---

## Postman Collection

### Create Environment
```json
{
  "id": "hms-env",
  "name": "HMS Development",
  "values": [
    {
      "key": "base_url",
      "value": "http://localhost:8080/api"
    },
    {
      "key": "patient_token",
      "value": ""
    },
    {
      "key": "doctor_token",
      "value": ""
    },
    {
      "key": "admin_token",
      "value": ""
    }
  ]
}
```

### Import Swagger
In Postman:
1. File → Import
2. URL: `http://localhost:8080/v3/api-docs`
3. Import as Swagger 2.0

---

## Database Inspection

### MySQL CLI Commands
```bash
# Connect
mysql -u hms_user -p hospital_management_system

# View all tables
SHOW TABLES;

# View users
SELECT id, username, email, role FROM users;

# View patients
SELECT id, blood_group, gender, admission_status FROM patients;

# View appointments
SELECT id, patient_id, doctor_id, appointment_status FROM appointments;

# Check invoices
SELECT id, invoice_number, total_amount, payment_status FROM invoices;

# View prescriptions
SELECT id, medicine_name, dosage, frequency FROM prescriptions;

# Check medicine inventory
SELECT id, name, quantity_in_stock, reorder_level FROM medicines;
```

---

## Troubleshooting

### Problem: Port 8080 already in use
```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>
```

### Problem: Database connection error
- Verify MySQL is running
- Check credentials in application.properties
- Ensure database exists: `CREATE DATABASE hospital_management_system;`

### Problem: JWT token invalid
- Token may have expired (24 hours)
- Login again to get new token
- Verify Bearer prefix in header

### Problem: Tests failing
```bash
# Clean and rebuild
mvn clean compile

# Run tests with verbose output
mvn test -e
```

---

## Performance Testing

### Apache JMeter
```bash
# Install JMeter
# Create test plan for appointment booking
# Set concurrent users: 100
# Ramp-up period: 60 seconds
# Loop count: 10
```

### Load Testing with Locust
```python
from locust import HttpUser, task, between

class HMSUser(HttpUser):
    wait_time = between(1, 5)
    
    @task
    def get_patients(self):
        self.client.get(
            "/patients",
            headers={"Authorization": "Bearer TOKEN"}
        )
```

---

## Monitoring & Logging

### Check Application Logs
```bash
# Tail logs
tail -f target/hms.log

# With grep
tail -f target/hms.log | grep ERROR
```

### Logging Configuration
Edit `application.properties`:
```properties
logging.level.com.hms=DEBUG
logging.file.name=target/hms.log
```

---

**Happy Testing! 🚀**
