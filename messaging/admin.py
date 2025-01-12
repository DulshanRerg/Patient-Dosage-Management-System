from django.contrib import admin
from .models import Doctor, Patient, Medicine, Dosage, Message

# Register your models here
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(Dosage)
admin.site.register(Message)