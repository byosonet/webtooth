from django.urls import path
from appfiles import views

urlpatterns=[
    path('list/file/', views.listarArchivo, name="listarArchivo"),
    path('add/file/', views.altaArchivo, name="altaArchivo"),
    path('delete/file/<int:idFile>/', views.eliminarArchivo, name="eliminarArchivo"),
]
