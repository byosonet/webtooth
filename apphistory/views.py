from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from webtooth.config import logger, getLogin, filterQueryUser_id
from . query import getGroup, getStudy, addHistory, delHistory, getHistory
from webtooth.decorators import validRequest
from apppatients import views
from django.contrib import messages
from apphistory.permissions import addGroup, viewGroup, updateGroup, deleteGroup, notPermission
from . models import Group

# Create your views here.
log = logger('apphistory', True)

def printLogHistory(register):
    log.debug(register)


def createHistoryGroup(request):
    printLogHistory("-- createHistoryGroup")
    return getGroup(request)

def createHistoryStudy(request):
    printLogHistory("-- createHistoryStudy")
    return getStudy(request)

def getAllHistoryByPatient(request,idPatient):
    printLogHistory("-- getAllHistoryByPatient")
    return getHistory(request,idPatient)

@validRequest
def updateHistory(request, idPatient):
    printLogHistory("-- Load updateHistory by idPatient: "+str(idPatient))
    try:
        if request.method == 'POST':
            log.debug("Method POST with params: "+str(request.POST))
            delHistory(idPatient)
            for p in request.POST:
                log.debug("field: {}, value: {}".format(p, request.POST.get(p)))
                if request.POST.get(p) == 'on':
                    log.info("Check recibido con id: {}".format(int(p)))
                    study = int(p)
                    addHistory(request, idPatient, study)
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo history: {}".format(ex))
    printLogHistory("Se redirige nuevamente a los datos del paciente")
    messages.success(request, "¡Los datos han sido actualizados correctamente!")
    return views.buscarId(request, idPatient)

@login_required(login_url=getLogin())
@permission_required(viewGroup(), login_url=notPermission())
@validRequest
def viewGroup(request):
    log.info("[Load view method: viewGroup]")
    listadoGrupos = Group.objects.filter(filterQueryUser_id()).order_by('-fechaAlta')   
    return render(request, "history/agregarGrupo.html", {"listadoGrupos": listadoGrupos})

@login_required(login_url=getLogin())
@permission_required(addGroup(), login_url=notPermission())
@validRequest
def addGroup(request):
    log.info("[Load view method: addGroup]")
    try:
        if request.method == 'POST':
            log.debug("Method POST with params: "+str(request.POST))
            params = []
            for p in request.POST:
                log.debug("field: {}, value: {}".format(p, request.POST.get(p)))
                if not p == "csrfmiddlewaretoken":
                    log.info("-- Add param: "+str(p))
                    params.append(p)
            if request.POST.get(params[0]):
                valueNameGroup = request.POST.get(params[0])
                log.info("Group name to process: {}".format(valueNameGroup))
                grupo = Group()
                grupo.nombre = valueNameGroup
                grupo.user = request.user
                grupo.save()
                messages.success(request, "¡Se ha agredado correctamente el grupo: {}!".format(valueNameGroup))
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo addGroup: {}".format(ex))
    printLogHistory("Se redirige nuevamente al listado de grupos")
    return redirect("viewGroup")
