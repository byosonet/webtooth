from django.urls import path
from apppatients import views

from django.views.decorators.csrf import csrf_exempt

URL_LISTAR_ARCHIVO = "listarArchivo"

urlpatterns=[
    path('search/', views.buscarPaciente, name="buscarPaciente"),
    path('search/name/',views.buscarNombre, name="buscarNombre"),
    path('list/patient/',views.listarPaciente, name="listarPaciente"),
    path('list/adress/',views.listarDireccion, name="listarDireccion"),
    path('add/', views.altaPaciente, name="altaPaciente"),
    path('search/<int:idPatient>/', views.buscarId, name="buscarId"),
    path('update/<int:idPatient>/', views.actualizarPaciente, name="actualizarPaciente"),
    path('delete/<int:idPatient>/', views.eliminarPaciente, name="eliminarPaciente"),
    
    ###Services example for angular
    path('patient/json/', views.jsonPatient, name="jsonPatient"),
    path('contact/add/json/', csrf_exempt(views.addContact), name="addContact"),
]
