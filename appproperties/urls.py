from django.urls import path
from appproperties import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('class/user/',csrf_exempt(views.updateClassMenu), name="updateClassMenu"),
    path('font/user/<str:value>',views.updateFontMenu, name="updateFontMenu"),
]
