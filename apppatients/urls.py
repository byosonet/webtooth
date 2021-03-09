from django.urls import path
from apppatients import views

from django.views.decorators.csrf import csrf_exempt

URL_LISTAR_ARCHIVO = "listarArchivo"

urlpatterns=[
    path('search/', views.buscarPaciente, name="buscarPaciente"),
    path('search/name/',views.buscarNombre, name="buscarNombre"),
    path('list/patient/',views.listarPaciente, name="listarPaciente"),
    path('list/adress/',views.listarDireccion, name="listarDireccion"),
    path('contact/',views.contactoPaciente, name="contactoPaciente"),
    path('add/', views.altaPaciente, name="altaPaciente"),
    path('search/<int:idPatient>/', views.buscarId, name="buscarId"),
    path('update/<int:idPatient>/', views.actualizarPaciente, name="actualizarPaciente"),
    path('delete/<int:idPatient>/', views.eliminarPaciente, name="eliminarPaciente"),

    path('import/patient/', views.importPatients, name="importPatients"),
    path('add/task/', views.altaTarea, name="altaTarea"),
    path('detail/task/<int:idTask>/', views.buscarTaskId, name="buscarTaskId"),
    path('update/task/<int:idTask>/', views.actualizarTask, name="actualizarTask"),
    path('email/patient/<int:idPatient>/',views.emailPatient, name="emailPatient"),
    
    ###Services example for angular
    path('patient/json/', views.jsonPatient, name="jsonPatient"),
    path('contact/add/json/', csrf_exempt(views.addContact), name="addContact"),
    ###ClassMenu
    path('class/user/',csrf_exempt(views.updateClassMenu), name="updateClassMenu"),
    path('font/user/<str:value>',views.updateFontMenu, name="updateFontMenu"),
]
