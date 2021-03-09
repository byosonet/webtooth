from django.urls import path
from apptasks import views

urlpatterns=[
    path('add/task/', views.altaTarea, name="altaTarea"),
    path('detail/task/<int:idTask>/', views.buscarTaskId, name="buscarTaskId"),
    path('update/task/<int:idTask>/', views.actualizarTask, name="actualizarTask"),
]
