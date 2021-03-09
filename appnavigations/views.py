from django.contrib.auth.decorators import login_required, permission_required
from webtooth.decorators import validRequest
from django.shortcuts import render
from django.conf import settings

from . models import Navigation

from appnavigations.permissions import *
from webtooth.config import logger, getLogin, filterQuery

# Create your views here.
log = logger('appnavigations', True)

@login_required(login_url=getLogin())
@permission_required(listNavigation(), login_url=notPermission())
@validRequest
def listarNavegacion(request):
    log.info("[Load view method: listarNavegacion]")
    log.info("Obteniendo lista de navegacion")    
    listadoNavegacion = Navigation.objects.filter(filterQuery()).order_by('-eventTime')[:settings.MAX_ROWS_QUERY_MODEL_NAVIGATION]
    return render(request, "navigation/listaNavegacion.html", {"listaNavegacion": listadoNavegacion})