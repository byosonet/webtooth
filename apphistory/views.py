from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from webtooth.config import logger, getLogin, filterQueryUser_id, currentLocalTime
from . query import getGroup, getStudy, addHistory, delHistory, getHistory
from webtooth.decorators import validRequest
from apppatients import views
from django.contrib import messages
from apphistory.permissions import addGroup, viewGroup, updateGroup, deleteGroup, notPermission, addStudy, viewStudy, updateStudy, deleteStudy
from . models import Group, Study

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
    return redirect("buscarId",idPatient=idPatient)

@login_required(login_url=getLogin())
@permission_required(viewGroup(), login_url=notPermission())
@validRequest
def viewGroup(request):
    log.info("[Load view method: viewGroup]")
    listadoGrupos = Group.objects.filter(filterQueryUser_id()).order_by('-fechaUpdate')   
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
                log.info("¡Se ha agredado correctamente el grupo: {}!".format(valueNameGroup))
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo addGroup: {}".format(ex))
    printLogHistory("Se redirige nuevamente al listado de grupos")
    return redirect("viewGroup")

@login_required(login_url=getLogin())
@permission_required(deleteGroup(), login_url=notPermission())
@validRequest
def deleteGroup(request, idGroup):
    log.info("[Load view method: deleteGroup]")
    try:
        grupo = Group.objects.get(pk=idGroup)
        valueNameGrp = grupo.nombre
        grupo.delete()
        messages.success(request, "¡Se ha eliminado correctamente el grupo: {}!".format(valueNameGrp))
        log.info("¡Se ha eliminado correctamente el grupo: {}!".format(valueNameGrp))
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo deleteGroup: {}".format(ex))
        messages.error(request, "¡No se ha podido eliminar el grupo: {}!".format(ex))
    printLogHistory("Se redirige nuevamente al listado de grupos")
    return redirect("viewGroup")

@login_required(login_url=getLogin())
@permission_required(updateGroup(), login_url=notPermission())
@validRequest
def editGroup(request, idGroup):
    log.info("[Load view method: editGroup]")
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
                newNameGroup = request.POST.get(params[0])
                log.info("Group name to update: {}".format(newNameGroup))
                grupo = Group.objects.get(pk=idGroup)
                nameOld = grupo.nombre
                grupo.nombre = newNameGroup
                grupo.fechaUpdate = currentLocalTime()
                grupo.save()
                messages.success(request, "¡Se ha actualizado correctamente el grupo de: {} a: {}!".format(nameOld,newNameGroup))
                log.info("¡Se ha actualizado correctamente el grupo de: {} a:{}!".format(nameOld,newNameGroup))
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo editGroup: {}".format(ex))
        messages.error(request, "¡No se ha podido actualizar el grupo: {}!".format(ex))
    printLogHistory("Se redirige nuevamente al listado de grupos")
    return redirect("viewGroup")


@login_required(login_url=getLogin())
@permission_required(viewStudy(), login_url=notPermission())
@validRequest
def viewStudy(request):
    log.info("[Load view method: viewStudy]")
    listadoEstudios = Study.objects.filter(filterQueryUser_id()).order_by('-fechaUpdate')   
    selectGrp = getGroup(request)
    return render(request, "history/agregarEstudio.html", {"listadoEstudios": listadoEstudios, "selectGrp":selectGrp})

@login_required(login_url=getLogin())
@permission_required(deleteStudy(), login_url=notPermission())
@validRequest
def deleteStudy(request, idStudy):
    log.info("[Load view method: deleteStudy]")
    try:
        estudio = Study.objects.get(pk=idStudy)
        valueNameStd = estudio.nombre
        estudio.delete()
        messages.success(request, "¡Se ha eliminado correctamente el estudio: {}!".format(valueNameStd))
        log.info("¡Se ha eliminado correctamente el estudio: {}!".format(valueNameStd))
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo deleteStudy: {}".format(ex))
        messages.error(request, "¡No se ha podido eliminar el estudio: {}!".format(ex))
    printLogHistory("Se redirige nuevamente al listado de estudios")
    return redirect("viewStudy")

@login_required(login_url=getLogin())
@permission_required(updateStudy(), login_url=notPermission())
@validRequest
def editStudy(request, idStudy):
    log.info("[Load view method: editStudy]")
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
                newNameStudy = request.POST.get(params[0])
                log.info("Study name to update: {}".format(newNameStudy))
                estudio = Study.objects.get(pk=idStudy)
                nameOld = estudio.nombre
                estudio.nombre = newNameStudy
                estudio.fechaUpdate = currentLocalTime()
                estudio.save()
                messages.success(request, "¡Se ha actualizado correctamente el estudio de: {} a: {}!".format(nameOld,newNameStudy))
                log.info("¡Se ha actualizado correctamente el estudio de: {} a:{}!".format(nameOld,newNameStudy))
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo editStudy: {}".format(ex))
        messages.error(request, "¡No se ha podido actualizar el estudio: {}!".format(ex))
    printLogHistory("Se redirige nuevamente al listado de estudios")
    return redirect("viewStudy")

@login_required(login_url=getLogin())
@permission_required(addStudy(), login_url=notPermission())
@validRequest
def addStudy(request):
    log.info("[Load view method: addStudy]")
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
                idGroup = int(request.POST.get(params[0]))
                grupo = Group.objects.get(pk=idGroup)
                valueNameStudy = request.POST.get(params[1])
                log.info("Study name to process: {}".format(valueNameStudy))
                estudio = Study()
                estudio.nombre = valueNameStudy
                estudio.user = request.user
                estudio.grupo = grupo
                estudio.save()
                messages.success(request, "¡Se ha agredado correctamente el estudio: {}!".format(valueNameStudy))
                log.info("¡Se ha agredado correctamente el estudio: {}!".format(valueNameStudy))
    except Exception as ex:
        log.error("-- No se pudo procesar el modulo addStudy: {}".format(ex))
    printLogHistory("Se redirige nuevamente al listado de estudios")
    return redirect("viewStudy")