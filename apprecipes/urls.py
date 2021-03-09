from django.urls import path
from apprecipes import views

urlpatterns=[
    path('contact/',views.contactoPaciente, name="contactoPaciente"),
    path('email/patient/<int:idPatient>/',views.emailPatient, name="emailPatient"),
]
