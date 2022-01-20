from webtooth.config import logger, currentLocalTime
from . models import Group, Study, History
from apppatients.models import Patient
from django.contrib.auth.models import User

log = logger('apphistory.query', False)
def printLogHistory(register):
    log.debug(register)

def getGroup(request):
    printLogHistory("Get list group")
    printLogHistory("Filter by user: "+str(request.user))
    listGroup = Group.objects.filter(user=request.user).order_by('fechaAlta')
    return listGroup

def getStudy(request):
    printLogHistory("Get list study")
    printLogHistory("Filter by user: "+str(request.user))
    listStudy = Study.objects.filter(user=request.user).order_by('fechaAlta')
    return listStudy

def getHistory(request, idPatient):
    printLogHistory("Get list history")
    printLogHistory("Filter by user: "+str(request.user))
    listHistory = History.objects.filter(user=request.user,patient_id=idPatient)
    listIdsHistory = []
    for his in listHistory:
        printLogHistory(his)
        listIdsHistory.append(his.estudio.id)
    return listIdsHistory

def getUserOfPatient(idPatient):
    patient = Patient.objects.get(pk=idPatient)
    return patient.userId

def getGroupByPatient(request, idPatient):
    printLogHistory("Get list group")
    printLogHistory("Filter by user: "+str(request.user))
    listGroup = Group.objects.filter(
        user=getUserOfPatient(idPatient)).order_by('fechaAlta')
    return listGroup

def getStudyByPatient(request, idPatient):
    printLogHistory("Get list study")
    printLogHistory("Filter by user: "+str(request.user))
    listStudy = Study.objects.filter(
        user=getUserOfPatient(idPatient)).order_by('fechaAlta')
    return listStudy

def getHistoryByPatient(request, idPatient):
    printLogHistory("Get list history")
    printLogHistory("Filter by user: "+str(request.user))
    listHistory = History.objects.filter(
        user=getUserOfPatient(idPatient), patient_id=idPatient)
    listIdsHistory = []
    for his in listHistory:
        printLogHistory(his)
        listIdsHistory.append(his.estudio.id)
    return listIdsHistory

def addHistory(idPatient,idStudy):
    study = Study.objects.get(pk=idStudy)
    patient = Patient.objects.get(pk=idPatient)
    history = History()
    history.patient = patient
    history.estudio = study
    user = User.objects.get(id=patient.userId)
    history.user = user
    history.grupo = study.grupo
    history.check = True
    history.save()

    patient.fechaUpdate = currentLocalTime()
    patient.save()
    log.info("-- Se ha añadido nuevo registro en history")

def delHistory(idPatient):
    try:
        History.objects.filter(patient_id=idPatient).delete()
        printLogHistory("-- Se han borrado los history del paciente: {}".format(idPatient))
    except Exception as ex:
        log.error("No se pudo borrar el historial de paciente: {}".format(ex))
        
def createGroupFirstOnly(request):
    
    listaGrupos = ['Examen de Tejidos (Duros)','Examen de Tejidos (Blandos)','Examen de Tejidos (Oclusión)','Motivo de Consulta','Habitos']
    listaEstudioGrupo1 = ['Esmalte','Raí­z','Dentina','Huesos']
    listaEstudioGrupo2 = ['Encía','Inserción','Epitelial (Migración)','Pulpa (Alteraciones)','Velo del Paladar','Carrillos']
    listaEstudioGrupo3 = ['Sobre Mordida Vertical','Mordida Abierta','Desgaste','Mal Oclusión','Intercuspideo','Desmayos','Mareos','Vertigos','Otros']
    listaEstudioGrupo4 = ['Emergencia','Revisión','Lesión Caries','Odontoxesis','Puente','Prostodoncia','Extracción','Malestares']
    listaEstudioGrupo5 = ['Bricomanía','Contracciones Musculares','Habitos de Mordida','Respiración Bucal','Chupadores de Labio','Lengua','Dedos']
    listIdsGrupos = []

    log.info("-- Creando grupos:")
    for grp in listaGrupos:
        grupo = Group()
        grupo.nombre = grp
        grupo.user = request.user
        grupo.save()
        listIdsGrupos.append(grupo.id)
        log.info("-- Grupo creado con el nombre: "+str(grp))

    log.info("-- Creando estudios:")
    grupo1 = Group.objects.get(pk=listIdsGrupos[0])
    for est1 in listaEstudioGrupo1:
        estudio = Study()
        estudio.nombre = est1
        estudio.user = request.user
        estudio.grupo = grupo1
        estudio.save()
        log.info("-- Estudio creado con el nombre: "+str(est1))

    grupo2 = Group.objects.get(pk=listIdsGrupos[1])
    for est2 in listaEstudioGrupo2:
        estudio = Study()
        estudio.nombre = est2
        estudio.user = request.user
        estudio.grupo = grupo2
        estudio.save()
        log.info("-- Estudio creado con el nombre: "+str(est2))

    grupo3 = Group.objects.get(pk=listIdsGrupos[2])
    for est3 in listaEstudioGrupo3:
        estudio = Study()
        estudio.nombre = est3
        estudio.user = request.user
        estudio.grupo = grupo3
        estudio.save()
        log.info("-- Estudio creado con el nombre: "+str(est3))

    grupo4 = Group.objects.get(pk=listIdsGrupos[3])
    for est4 in listaEstudioGrupo4:
        estudio = Study()
        estudio.nombre = est4
        estudio.user = request.user
        estudio.grupo = grupo4
        estudio.save()
        log.info("-- Estudio creado con el nombre: "+str(est4))

    grupo5 = Group.objects.get(pk=listIdsGrupos[4])
    for est5 in listaEstudioGrupo5:
        estudio = Study()
        estudio.nombre = est5
        estudio.user = request.user
        estudio.grupo = grupo5
        estudio.save()
        log.info("-- Estudio creado con el nombre: "+str(est5))
