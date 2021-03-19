"""webtooth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from webtooth.views import homeView, error404, notHasPermission, color

admin.site.site_header = 'Webtooth'
admin.site.index_title = 'Consola de administración'
admin.site.site_title = 'Webtooth'
admin.site.site_url = '/webtooth/'

urlpatterns = [
    path('', homeView, name="home"),
    path('color/<int:idColor>/', color, name="color"),
    path('admin/', admin.site.urls, name="admin"),

    #Urls apppatients
    path('service/', include('apppatients.urls')),
    #Urls appfiles
    path('service/', include('appfiles.urls')),
    #Urls appnavigations
    path('service/', include('appnavigations.urls')),
    #Urls appimports
    path('service/', include('appimports.urls')),
    #Urls apptasks
    path('service/', include('apptasks.urls')),
    #Urls apprecipes
    path('service/', include('apprecipes.urls')),
    #Urls appproperties
    path('service/', include('appproperties.urls')),
    #Urls appphistory
    path('service/', include('apphistory.urls')),

    #UrlsNotHasPermissions
    path('permission/required/', notHasPermission, name="notpermission"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#Excepciones when Debug is False
handler404 = error404
