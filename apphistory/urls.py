from django.urls import path
from apphistory import views

urlpatterns=[
    path('update/history/<int:idPatient>/', views.updateHistory, name="updateHistory"),
    path('add/group/', views.addGroup, name="addGroup"),
]
