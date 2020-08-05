from django.urls import path
from appGestionPacientes import views

URL_LISTAR_ARCHIVO = "listarArchivo"

urlpatterns=[
    path('search/', views.buscarPaciente, name="buscarPaciente"),
    path('search/name/',views.buscarNombre, name="buscarNombre"),
    path('list/patient/',views.listarPaciente, name="listarPaciente"),
    path('list/navigation/', views.listarNavegacion, name="listarNavegacion"),
    path('list/adress/',views.listarDireccion, name="listarDireccion"),
    path('list/file/', views.listarArchivo, name=URL_LISTAR_ARCHIVO),
    path('contact/',views.contactoPaciente, name="contactoPaciente"),
    path('add/', views.altaPaciente, name="altaPaciente"),
    path('add/file/', views.altaArchivo, name="altaArchivo"),
    path('search/<int:idPatient>/', views.buscarId, name="buscarId"),
    path('update/<int:idPatient>/', views.actualizarPaciente, name="actualizarPaciente"),
    path('delete/<int:idPatient>/', views.eliminarPaciente, name="eliminarPaciente"),
    path('delete/file/<int:idFile>/', views.eliminarArchivo, name="eliminarArchivo"),
]
