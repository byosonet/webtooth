from django.urls import path
from apphistory import views

urlpatterns=[
    path('update/history/<int:idPatient>/', views.updateHistory, name="updateHistory"),
    path('view/group/', views.viewGroup, name="viewGroup"),
    path('add/group/', views.addGroup, name="addGroup"),
    path('delete/group/<int:idGroup>', views.deleteGroup, name="deleteGroup"),
    path('edit/group/<int:idGroup>', views.editGroup, name="editGroup"),
    path('view/study/', views.viewStudy, name="viewStudy"),
    path('delete/study/<int:idStudy>', views.deleteStudy, name="deleteStudy"),
    path('edit/study/<int:idStudy>', views.editStudy, name="editStudy"),
    path('add/study/', views.addStudy, name="addStudy"),
]
