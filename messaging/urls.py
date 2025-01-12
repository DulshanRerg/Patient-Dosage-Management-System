from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_register_view, name='login_register'),
    path('verify/<uuid:token>/', views.verify_email_view, name='verify_email'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('messages/', views.message_view, name='messages'),
    path('add-patient/', views.add_patient, name='add-patient'),  # Ensure this matches the name used in the template
    path('add-medicine/', views.add_medicine, name='add-medicine'),
    path('assign-dosage/', views.assign_dosage_view, name='assign-dosage'),
    path('send-messages/', views.message_view, name='send-messages'),
    path('logout/',views.logout_view, name='logout'),
]