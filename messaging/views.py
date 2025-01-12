from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.timezone import now
from django.db import IntegrityError
from .forms import PatientForm, MedicineForm
import re, phonenumbers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password # For password hashing
from .models import Doctor, Patient, Medicine, Dosage, Message

# Doctor Login View
def login_register_view(request):
    error = None
    success = None

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'signin':
            # Login logic
            email = request.POST.get('email')
            password = request.POST.get('password')
            doctor = Doctor.objects.filter(email=email).first()

            if doctor and check_password(password, doctor.password):
                request.session['doctor_id'] = doctor.id

                # Redirect to 'next' parameter or dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                error = "Invalid email or password."

        elif form_type == 'signup':
            # Registration logic
            fullname = request.POST.get('fullname')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                parsed_phone = phonenumbers.parse(phone)
                if not phonenumbers.is_valid_number(parsed_phone):
                    error = "The phone number is not valid."
                    return render(request, 'login.html', {'error': error, 'success': success})
            except phonenumbers.NumberParseException:
                error = "The phone number format is invalid."
                return render(request, 'login.html', {'error': error, 'success': success})

            # Check for duplicate email or phone number

            # Check if email is already registered
            if Doctor.objects.filter(email=email).exists():
                error = "Email is already registered."
            elif Doctor.objects.filter(phone_number=phone).exists():
                error = "Phone number is already registered."
            elif len(password) < 8:
                error = "Password must be at least 8 characters long."
            elif not re.search(r'[A-Z]', password):
                error = "Password must contain at least one uppercase letter."
            elif not re.search(r'[a-z]', password):
                error = "Password must contain at least one lowercase letter."
            elif not re.search(r'[0-9]', password):
                error = "Password must contain at least one digit."
            elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                error = "Password must contain at least one special character (!@#$%^&*(), etc.)."
            else:
                # Create the doctor account
                try:
                    doctor = Doctor.objects.create(
                    name=fullname,
                    phone_number=phone,
                    email=email,
                    password=make_password(password),
                    is_active = False #Inactive until verified
                    )
                except IntegrityError:
                    error = "A doctor with this email or phone number already exists."

                # Send email verification
                verification_link = f"http://127.0.0.1:8000/verify/{doctor.email_token}/"
                try:
                    send_mail(
                        'Subject',
                        'Message body',
                        settings.EMAIL_HOST_USER,
                        ['recipient@example.com'],
                        fail_silently=False,
                     )
                except Exception as e:
                    print(f"Email sending failed: {e}")

                success = "Registration successful! Please verify your email to activate your account."

    return render(request, 'login.html', {'error': error, 'success': success})

#Email Verification
def verify_email_view(request, token):
    doctor = Doctor.objects.filter(email_token=token).first()
    if not doctor:
        return render(request, 'email_verification_failed.html')

    doctor.is_active = True
    doctor.email_token = None
    doctor.save()
    return render(request, 'email_verification_success.html')

#Dashboard View
# @login_required
def dashboard_view(request):
    if not request.session.get('doctor_id'):
        return redirect('login')

    doctor_id = request.session['doctor_id']
    doctor = Doctor.objects.get(id=doctor_id)
    patients = Patient.objects.filter(doctor=doctor)

    # Data for the dashboard
    total_patients = patients.count()
    total_medicines = Dosage.objects.filter(patient__in=patients).count()
    recent_messages = Message.objects.filter(doctor=doctor).order_by('-timestamp')[:5]

    context = {
        'doctor': doctor,
        'patients': patients,
        'total_patients': total_patients,
        'total_medicines': total_medicines,
        'recent_messages': recent_messages,
    }
    return render(request, 'messaging/dashboard.html', context)

# Assign Dosage
def assign_dosage_view(request):
    if not request.session.get('doctor_id'):
        return redirect('login')
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        medicine_id = request.POST.get('medicine')
        dosage_time = request.POST.get('time')
        dosage_quantity = request.POST.get('quantity')

        Dosage.objects.create(
            patient_id=patient_id,
            medicine_id=medicine_id,
            dosage_time=dosage_time,
            dosage_quantity=dosage_quantity,
        )
        return redirect('dashboard')
    doctor = Doctor.objects.get(id=request.session['doctor_id'])
    patients = Patient.objects.filter(doctor=doctor)
    medicines = Medicine.objects.all()
    return render(request, 'messaging/assign_dosage.html', {'patients': patients, 'medicines': medicines})

# Messaging View
def message_view(request):
    if not request.session.get('doctor_id'):
        return redirect('login')
    if request.method == 'POST':
        patient_ids = request.POST.getlist('patients')
        content = request.POST.get('message')
        schedule_time = request.POST.get('schedule_time')

        #Immediate or scheduled meesage logic
        if schedule_time:
            print(f"Scheduling message for {schedule_time}: {content}")
        else:
            for patient_id in patient_ids:
                patient = Patient.objects.get(id=patient_id)
                # send_sms(patient.phone_number, content)
                print(f"Message sent to {patient.name} ({patient.phone_number}): {content}")
        return redirect(request, 'dashboard')

        Message.objects.create(
            doctor_id=request.session['doctor_id'],
            patient_id=patient_id,
            content=content,
        )
        return redirect('dashboard')
    patients = Patient.objects.all()
    return render(request, 'messaging/messages.html', {'patients': patients})

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to dashboard after success
    else:
        form = PatientForm()
    return render(request, 'messaging/add_patient.html', {'form': form})

def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        Medicine.objects.create(name=name, description=description)
        return redirect('dashboard')
    return render(request, 'messaging/add_medicine.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login_register')
    return render(request, 'logout_confirm.html')
