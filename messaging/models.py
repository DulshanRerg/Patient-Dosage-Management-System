from django.db import models
import uuid

# Doctor Model
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    email_token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Patient Model (formerly User)
class Patient(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # Link patients to doctors
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Medicine Model
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Dosage Model
class Dosage(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True)  # Allow nulls
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage_time = models.DateTimeField()
    dosage_quantity = models.IntegerField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Taken', 'Taken'),
            ('Missed', 'Missed'),
        ],
        default='Pending'
    )

    def __str__(self):
        return f"{self.patient} - {self.medicine}"


# Message Model (for communication between doctor and patient)
class Message(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.doctor.name} to {self.patient.name}"