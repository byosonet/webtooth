from webtooth.config import logger
from . models import Group, Study, History
from apppatients.models import Patient

log = logger('apphistory.query', False)
def printLogHistory(register):
    log.debug(register)

def getGroup(request):
    printLogHistory("Get list group")
    printLogHistory("Filter by user: "+str(request.user))
    listGroup = Group.objects.filter(user=request.user)
    return listGroup

def getStudy(request):
    printLogHistory("Get list study")
    printLogHistory("Filter by user: "+str(request.user))
    listStudy = Study.objects.filter(user=request.user)
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

def addHistory(request,idPatient,idStudy):
    study = Study.objects.get(pk=idStudy)
    patient = Patient.objects.get(pk=idPatient)
    history = History()
    history.patient = patient
    history.estudio = study
    history.user = request.user
    history.grupo = study.grupo
    history.check = True
    history.save()
    log.info("-- Se ha añadido nuevo registro en history")

def delHistory(idPatient):
    try:
        History.objects.filter(patient_id=idPatient).delete()
        printLogHistory("-- Se han borrado los history del paciente: {}".format(idPatient))
    except Exception as ex:
        log.error("No se pudo borrar el historial de paciente: {}".format(ex))


    
