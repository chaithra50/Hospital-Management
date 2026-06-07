#!/usr/bin/env python3
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8080/api"
TOKEN = "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0ZXN0X2FkbWluX2ZpbmFsIiwiaWF0IjoxNzgwNTA4OTk0LCJleHAiOjE3ODA1OTUzOTR9.FnH0PK0OgbHwgNzHXRLkp1DIypbrMykODtlWxMeYCqoRdvBSsY3T1f7M3ACouUqkngZxxMxjbkIW_ul_Ty07GA"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

print("=" * 60)
print("TESTING HOSPITAL MANAGEMENT SYSTEM - DATA ENTRY")
print("=" * 60)

# 1. CREATE PATIENTS
print("\n1. CREATING PATIENTS...")
patients = [
    {
        "firstName": "Rajesh",
        "lastName": "Patel",
        "email": "rajesh.patel@email.com",
        "phoneNumber": "9876543210",
        "dateOfBirth": "1985-05-15",
        "gender": "M"
    },
    {
        "firstName": "Ananya",
        "lastName": "Gupta",
        "email": "ananya.gupta@email.com",
        "phoneNumber": "9123456789",
        "dateOfBirth": "1990-08-22",
        "gender": "F"
    }
]

patient_ids = []
for patient in patients:
    response = requests.post(f"{BASE_URL}/patients", json=patient, headers=HEADERS)
    if response.status_code == 201:
        data = response.json()
        patient_ids.append(data.get('id'))
        print(f"  ✓ Created patient: {patient['firstName']} {patient['lastName']} (ID: {data.get('id')})")
    else:
        print(f"  ✗ Failed to create patient {patient['firstName']}: Status {response.status_code} - {response.text[:100]}")

# 2. CREATE DOCTORS
print("\n2. CREATING DOCTORS...")
doctors = [
    {
        "firstName": "Vikram",
        "lastName": "Singh",
        "email": "dr.vikram@hospital.com",
        "specialization": "Cardiology",
        "yearsOfExperience": 12,
        "consultationFee": 500
    },
    {
        "firstName": "Neha",
        "lastName": "Sharma",
        "email": "dr.neha@hospital.com",
        "specialization": "Orthopedics",
        "yearsOfExperience": 8,
        "consultationFee": 400
    }
]

doctor_ids = []
for doctor in doctors:
    response = requests.post(f"{BASE_URL}/doctors", json=doctor, headers=HEADERS)
    if response.status_code == 201:
        data = response.json()
        doctor_ids.append(data.get('id'))
        print(f"  ✓ Created doctor: Dr. {doctor['firstName']} {doctor['lastName']} - {doctor['specialization']} (ID: {data.get('id')})")
    else:
        print(f"  ✗ Failed to create doctor {doctor['firstName']}: Status {response.status_code} - {response.text[:100]}")

# 3. CREATE APPOINTMENTS
print("\n3. CREATING APPOINTMENTS...")
if patient_ids and doctor_ids:
    appointments = [
        {
            "patientId": patient_ids[0],
            "doctorId": doctor_ids[0],
            "appointmentDate": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "appointmentTime": "10:00",
            "reasonForVisit": "Regular heart checkup"
        },
        {
            "patientId": patient_ids[1],
            "doctorId": doctor_ids[1],
            "appointmentDate": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "appointmentTime": "14:00",
            "reasonForVisit": "Knee pain treatment"
        }
    ]
    
    appointment_ids = []
    for appt in appointments:
        response = requests.post(f"{BASE_URL}/appointments", json=appt, headers=HEADERS)
        if response.status_code == 201:
            data = response.json()
            appointment_ids.append(data.get('id'))
            print(f"  ✓ Created appointment: {appt['appointmentDate']} - {appt['reasonForVisit']} (ID: {data.get('id')})")
        else:
            print(f"  ✗ Failed to create appointment: Status {response.status_code} - {response.text[:100]}")
    
    # 4. CREATE INVOICES
    print("\n4. CREATING INVOICES...")
    invoices = [
        {
            "patientId": patient_ids[0],
            "totalAmount": 2500,
            "paymentStatus": "PENDING",
            "invoiceDate": datetime.now().strftime("%Y-%m-%d")
        },
        {
            "patientId": patient_ids[1],
            "totalAmount": 1500,
            "paymentStatus": "PAID",
            "invoiceDate": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
        }
    ]
    
    for invoice in invoices:
        response = requests.post(f"{BASE_URL}/billing", json=invoice, headers=HEADERS)
        if response.status_code == 201:
            data = response.json()
            print(f"  ✓ Created invoice for patient ID {invoice['patientId']}: ₹{invoice['totalAmount']} - {invoice['paymentStatus']}")
        else:
            print(f"  ✗ Failed to create invoice: Status {response.status_code} - {response.text[:100]}")

print("\n" + "=" * 60)
print("DATA CREATION COMPLETE")
print("=" * 60)

# 5. VERIFY DATA
print("\n5. VERIFYING DATA IN DATABASE...")
print("\nGET /patients:")
response = requests.get(f"{BASE_URL}/patients", headers=HEADERS)
if response.status_code == 200:
    data = response.json()
    print(f"  Total patients: {data.get('totalElements', len(data))}")
    for p in data.get('content', data)[:2]:
        print(f"    - {p.get('firstName')} {p.get('lastName')} ({p.get('email')})")

print("\nGET /doctors:")
response = requests.get(f"{BASE_URL}/doctors", headers=HEADERS)
if response.status_code == 200:
    data = response.json()
    print(f"  Total doctors: {data.get('totalElements', len(data))}")
    for d in data.get('content', data)[:2]:
        print(f"    - Dr. {d.get('firstName')} {d.get('lastName')} - {d.get('specialization')} (₹{d.get('consultationFee')})")

print("\nGET /appointments:")
response = requests.get(f"{BASE_URL}/appointments", headers=HEADERS)
if response.status_code == 200:
    data = response.json()
    print(f"  Total appointments: {data.get('totalElements', len(data))}")
    for a in data.get('content', data)[:2]:
        print(f"    - {a.get('appointmentDate')} - {a.get('patientName')} with {a.get('doctorName')} ({a.get('appointmentStatus')})")

print("\nGET /billing:")
response = requests.get(f"{BASE_URL}/billing", headers=HEADERS)
if response.status_code == 200:
    data = response.json()
    print(f"  Total invoices: {data.get('totalElements', len(data))}")
    for inv in data.get('content', data)[:2]:
        print(f"    - INV-{inv.get('id')}: ₹{inv.get('totalAmount')} - {inv.get('paymentStatus')}")

print("\n" + "=" * 60)
