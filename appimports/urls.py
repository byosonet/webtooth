from django.urls import path
from appimports import views

urlpatterns=[
    path('import/patient/', views.importPatients, name="importPatients"),
]
