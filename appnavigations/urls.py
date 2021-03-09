from django.urls import path
from appnavigations import views

urlpatterns=[
    path('list/navigation/', views.listarNavegacion, name="listarNavegacion"),
]
