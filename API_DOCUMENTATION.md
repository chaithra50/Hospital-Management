# Hospital Management System - API Documentation

Complete REST API documentation with curl examples and request/response models.

## Base URL
```
http://localhost:8080/api
```

## Authentication

All protected endpoints require Bearer JWT token in Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzUxMiJ9...
```

---

## 1. Authentication Endpoints

### 1.1 Register User

**Endpoint:** `POST /auth/register`

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePassword123!",
  "firstName": "John",
  "lastName": "Doe",
  "phoneNumber": "9876543210",
  "role": "PATIENT"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123!",
    "firstName": "John",
    "lastName": "Doe",
    "phoneNumber": "9876543210",
    "role": "PATIENT"
  }'
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user_id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "role": "PATIENT",
  "first_name": "John",
  "last_name": "Doe",
  "message": "User registered successfully"
}
```

---

### 1.2 Login

**Endpoint:** `POST /auth/login`

**Request Body:**
```json
{
  "usernameOrEmail": "john_doe",
  "password": "SecurePassword123!"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "usernameOrEmail": "john_doe",
    "password": "SecurePassword123!"
  }'
```

**Response (200 OK):**
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

---

### 1.3 Get Current Profile

**Endpoint:** `GET /auth/profile`

**Headers:** 
```
Authorization: Bearer {token}
```

**cURL:**
```bash
curl -X GET http://localhost:8080/api/auth/profile \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "phoneNumber": "9876543210",
  "role": "PATIENT",
  "active": true,
  "emailVerified": false
}
```

---

### 1.4 Change Password

**Endpoint:** `POST /auth/change-password/{userId}`

**Request Body:**
```json
{
  "oldPassword": "SecurePassword123!",
  "newPassword": "NewPassword456!"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/auth/change-password/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "oldPassword": "SecurePassword123!",
    "newPassword": "NewPassword456!"
  }'
```

---

## 2. Patient Endpoints

### 2.1 Register Patient

**Endpoint:** `POST /patients/register`

**Request Body:**
```json
{
  "firstName": "Jane",
  "lastName": "Smith",
  "email": "jane.smith@example.com",
  "phoneNumber": "9876543211",
  "bloodGroup": "O+",
  "gender": "FEMALE",
  "dateOfBirth": "1990-05-15",
  "allergies": "Penicillin",
  "medicalConditions": "Diabetes",
  "emergencyContactName": "John Smith",
  "emergencyContactPhone": "9876543210"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/patients/register \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Smith",
    "email": "jane.smith@example.com",
    "phoneNumber": "9876543211",
    "bloodGroup": "O+",
    "gender": "FEMALE",
    "dateOfBirth": "1990-05-15",
    "allergies": "Penicillin",
    "medicalConditions": "Diabetes",
    "emergencyContactName": "John Smith",
    "emergencyContactPhone": "9876543210"
  }'
```

---

### 2.2 Get Patient Details

**Endpoint:** `GET /patients/{patientId}`

**cURL:**
```bash
curl -X GET http://localhost:8080/api/patients/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 2.3 Admit Patient

**Endpoint:** `POST /patients/{patientId}/admit`

**Request Body:**
```json
{
  "wardNumber": "101",
  "bedNumber": "5",
  "reasonForAdmission": "Acute Bronchitis",
  "expectedDischargeDate": "2024-06-15"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/patients/1/admit \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "wardNumber": "101",
    "bedNumber": "5",
    "reasonForAdmission": "Acute Bronchitis",
    "expectedDischargeDate": "2024-06-15"
  }'
```

---

### 2.4 Get All Patients (Paginated)

**Endpoint:** `GET /patients?page=0&size=20&sort=createdAt,desc`

**cURL:**
```bash
curl -X GET "http://localhost:8080/api/patients?page=0&size=20&sort=createdAt,desc" \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

## 3. Doctor Endpoints

### 3.1 Register Doctor

**Endpoint:** `POST /doctors/register`

**Request Body:**
```json
{
  "firstName": "Dr. James",
  "lastName": "Wilson",
  "email": "james.wilson@hospital.com",
  "phoneNumber": "9876543212",
  "specialization": "Cardiology",
  "licenseNumber": "LIC123456",
  "yearsOfExperience": 15,
  "department": "Cardiology",
  "consultationFee": 500.00
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/doctors/register \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Dr. James",
    "lastName": "Wilson",
    "email": "james.wilson@hospital.com",
    "phoneNumber": "9876543212",
    "specialization": "Cardiology",
    "licenseNumber": "LIC123456",
    "yearsOfExperience": 15,
    "department": "Cardiology",
    "consultationFee": 500.00
  }'
```

---

### 3.2 Get Available Doctors

**Endpoint:** `GET /doctors/available`

**cURL:**
```bash
curl -X GET http://localhost:8080/api/doctors/available \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 3.3 Get Doctors by Specialization

**Endpoint:** `GET /doctors/specialization/Cardiology`

**cURL:**
```bash
curl -X GET http://localhost:8080/api/doctors/specialization/Cardiology \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 3.4 Add Doctor Schedule

**Endpoint:** `POST /doctors/{doctorId}/schedules`

**Request Body:**
```json
{
  "doctorId": 1,
  "dayOfWeek": "MONDAY",
  "startTime": "09:00",
  "endTime": "17:00",
  "slotDurationMinutes": 30
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/doctors/1/schedules \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "doctorId": 1,
    "dayOfWeek": "MONDAY",
    "startTime": "09:00",
    "endTime": "17:00",
    "slotDurationMinutes": 30
  }'
```

---

## 4. Appointment Endpoints

### 4.1 Book Appointment

**Endpoint:** `POST /appointments`

**Request Body:**
```json
{
  "patientId": 1,
  "doctorId": 1,
  "appointmentDate": "2024-06-20T14:30:00",
  "reasonForVisit": "Regular Checkup",
  "notes": "Patient has hypertension history"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/appointments \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": 1,
    "doctorId": 1,
    "appointmentDate": "2024-06-20T14:30:00",
    "reasonForVisit": "Regular Checkup",
    "notes": "Patient has hypertension history"
  }'
```

**Response (201 Created):**
```json
{
  "id": 1,
  "patientId": 1,
  "patientName": "Jane Smith",
  "doctorId": 1,
  "doctorName": "Dr. James Wilson",
  "appointmentDate": "2024-06-20T14:30:00",
  "appointmentStatus": "SCHEDULED",
  "reasonForVisit": "Regular Checkup",
  "notes": "Patient has hypertension history"
}
```

---

### 4.2 Cancel Appointment

**Endpoint:** `POST /appointments/{appointmentId}/cancel`

**cURL:**
```bash
curl -X POST http://localhost:8080/api/appointments/1/cancel \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 4.3 Reschedule Appointment

**Endpoint:** `POST /appointments/{appointmentId}/reschedule?newDate=2024-06-21T15:00:00`

**cURL:**
```bash
curl -X POST "http://localhost:8080/api/appointments/1/reschedule?newDate=2024-06-21T15:00:00" \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 4.4 Complete Appointment

**Endpoint:** `POST /appointments/{appointmentId}/complete`

**cURL:**
```bash
curl -X POST http://localhost:8080/api/appointments/1/complete \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

## 5. Billing Endpoints

### 5.1 Create Invoice

**Endpoint:** `POST /billing/invoices?appointmentId=1&amount=5000.00`

**cURL:**
```bash
curl -X POST "http://localhost:8080/api/billing/invoices?appointmentId=1&amount=5000.00" \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 5.2 Record Payment

**Endpoint:** `POST /billing/invoices/{invoiceId}/payment?amount=2500.00`

**cURL:**
```bash
curl -X POST "http://localhost:8080/api/billing/invoices/1/payment?amount=2500.00" \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 5.3 Get Patient Invoices

**Endpoint:** `GET /billing/invoices/patient/{patientId}?page=0&size=20`

**cURL:**
```bash
curl -X GET "http://localhost:8080/api/billing/invoices/patient/1?page=0&size=20" \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

## 6. Medical Records Endpoints

### 6.1 Add Prescription

**Endpoint:** `POST /medical-records/prescriptions`

**Request Body:**
```json
{
  "appointmentId": 1,
  "medicineName": "Aspirin",
  "dosage": "500mg",
  "frequency": "Twice daily",
  "durationDays": 7,
  "quantity": 14,
  "instructions": "Take with food"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/medical-records/prescriptions \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "appointmentId": 1,
    "medicineName": "Aspirin",
    "dosage": "500mg",
    "frequency": "Twice daily",
    "durationDays": 7,
    "quantity": 14,
    "instructions": "Take with food"
  }'
```

---

### 6.2 Get Patient Prescriptions

**Endpoint:** `GET /medical-records/prescriptions/patient/{patientId}`

**cURL:**
```bash
curl -X GET http://localhost:8080/api/medical-records/prescriptions/patient/1 \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

## 7. Inventory Endpoints

### 7.1 Add Medicine

**Endpoint:** `POST /inventory/medicines`

**Request Body:**
```json
{
  "name": "Aspirin",
  "description": "Pain reliever and anti-inflammatory",
  "manufacturer": "PharmaCorp",
  "unitPrice": 50.00,
  "quantityInStock": 100,
  "reorderLevel": 20,
  "expiryDate": "2026-05-22"
}
```

**cURL:**
```bash
curl -X POST http://localhost:8080/api/inventory/medicines \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..." \
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

---

### 7.2 Update Medicine Stock

**Endpoint:** `PUT /inventory/medicines/{medicineId}/stock?quantity=50`

**cURL:**
```bash
curl -X PUT "http://localhost:8080/api/inventory/medicines/1/stock?quantity=50" \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 7.3 Get Low Stock Medicines

**Endpoint:** `GET /inventory/medicines/stock/low`

**cURL:**
```bash
curl -X GET http://localhost:8080/api/inventory/medicines/stock/low \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 7.4 Get Expired Medicines

**Endpoint:** `GET /inventory/medicines/expired`

**cURL:**
```bash
curl -X GET http://localhost:8080/api/inventory/medicines/expired \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

### 7.5 Search Medicines

**Endpoint:** `GET /inventory/medicines/search?name=Aspirin&page=0&size=20`

**cURL:**
```bash
curl -X GET "http://localhost:8080/api/inventory/medicines/search?name=Aspirin&page=0&size=20" \
  -H "Authorization: Bearer eyJhbGciOiJIUzUxMiJ9..."
```

---

## Error Response Format

All errors follow this standard format:

```json
{
  "status": 400,
  "message": "Validation failed",
  "error": "Validation Error",
  "timestamp": "2024-05-22T10:30:00",
  "path": "/api/patients/register",
  "fieldErrors": {
    "email": "Email is invalid",
    "phoneNumber": "Phone number must be 10 digits"
  }
}
```

---

## Common HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource
- `500 Internal Server Error` - Server error

---

## Testing with Postman

1. Import the collection from Swagger: `http://localhost:8080/v3/api-docs`
2. Set the `authorization_token` environment variable with the Bearer token
3. Use `{{authorization_token}}` in Authorization headers

---

**Last Updated:** May 2024
