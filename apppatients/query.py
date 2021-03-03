from apppatients.models import Patient, Adress, Task
from django.db.models import Q
from apppatients.signals import getUser

import uuid
from datetime import date

from webtooth.config import logger
log = logger('apppatients.config', False)

def filterSearch(request):
	listadoPacientes = None
	user = getUser()
	if request.POST.get('txtsearch'):
		txtSearch = request.POST['txtsearch']
		log.info("Realizando búsqueda desde home: >>> "+str(txtSearch))
		listadoPacientes = Patient.objects.filter(
			Q(nombre__icontains=txtSearch) |
			Q(apellidoPaterno__icontains=txtSearch) |
			Q(apellidoMaterno__icontains=txtSearch) |
			Q(email__icontains=txtSearch) |
			Q(telefono__icontains=txtSearch) |
			Q(numexp__icontains=txtSearch)).filter(userId=user.id)
	else:
		log.info("Realizando búsqueda desde menu")
		if request.POST.get('name') and not request.POST.get('apellidos') and not request.POST.get('numexp'):
			name = request.POST['name']
			log.info("Buscando solo por nombre: >>> "+str(name))
			listadoPacientes = Patient.objects.filter(
				Q(nombre__icontains=name)).filter(userId=user.id)
		elif not request.POST.get('name') and request.POST.get('apellidos') and not request.POST.get('numexp'):			
			apellidos = request.POST['apellidos']
			log.info("Buscando solo por apellidos: >>> "+str(apellidos))
			listadoPacientes = Patient.objects.filter(
				Q(apellidoPaterno__icontains=apellidos) |
				Q(apellidoMaterno__icontains=apellidos)).filter(userId=user.id)
		elif not request.POST.get('name') and not request.POST.get('apellidos') and request.POST.get('numexp'):			
			numexp = request.POST['numexp']
			log.info("Buscando solo por expediente: >>> "+str(numexp))
			listadoPacientes = Patient.objects.filter(
				Q(numexp__icontains=numexp)).filter(userId=user.id)
		elif request.POST.get('name') and request.POST.get('apellidos') and not request.POST.get('numexp'):			
			name = request.POST['name']			
			apellidos = request.POST['apellidos']
			log.info("Buscando solo por nombre y apellidos: >>> {} {}".format(name,apellidos))
			listadoPacientes = Patient.objects.filter(
				Q(nombre__icontains=name) |
				Q(apellidoPaterno__icontains=apellidos) |
				Q(apellidoMaterno__icontains=apellidos)).filter(userId=user.id)
		elif request.POST.get('name') and not request.POST.get('apellidos') and request.POST.get('numexp'):			
			name = request.POST['name']
			numexp = request.POST['numexp']
			log.info("Buscando solo por nombre y expediente: >>> {} {}".format(name,numexp))
			listadoPacientes = Patient.objects.filter(
				Q(nombre__icontains=name) |
				Q(numexp__icontains=numexp)).filter(userId=user.id)
		elif not request.POST.get('name') and request.POST.get('apellidos') and request.POST.get('numexp'):			
			apellidos = request.POST['apellidos']
			numexp = request.POST['numexp']
			log.info("Buscando solo por apellidos y expediente: >>> {} {}".format(apellidos, numexp))
			listadoPacientes = Patient.objects.filter(
				Q(apellidoPaterno__icontains=apellidos) |
				Q(apellidoMaterno__icontains=apellidos) |
				Q(numexp__icontains=numexp)).filter(userId=user.id)
		elif request.POST.get('name') and request.POST.get('apellidos') and request.POST.get('numexp'):			
			name = request.POST['name']
			apellidos = request.POST['apellidos']
			numexp = request.POST['numexp']
			log.info("Buscando por todos los campos: >>> {} {} {}".format(name,apellidos,numexp))
			listadoPacientes = Patient.objects.filter(
				Q(nombre__icontains=name) |
				Q(apellidoPaterno__icontains=apellidos) |
				Q(apellidoMaterno__icontains=apellidos) |
				Q(numexp__icontains=numexp)).filter(userId=user.id)
		else:
			log.info("Ningún dato ha sido enviado para buscar")

	if listadoPacientes:
		for i, p in enumerate(listadoPacientes):
			printLogQuery("{}.- {}, expediente: {}, correo: {}".format(i,p.nombre, p.numexp, p.email))
	return listadoPacientes


def filterByIdPatient(idPatient, formPatient):
	printLogQuery("Id recibido for patient: "+str(idPatient))
	user = getUser()	
	patient = Patient.objects.get(pk=idPatient, userId=user.id)
	if patient:
		log.info("Paciente encontrado: {} {}".format(
			patient.nombre, patient.apellidoPaterno))
		formPatient.fields['nombre'].initial = patient.nombre
		formPatient.fields['apellidoPaterno'].initial = patient.apellidoPaterno
		formPatient.fields['apellidoMaterno'].initial = patient.apellidoMaterno
		formPatient.fields['email'].initial = patient.email
		formPatient.fields['telefono'].initial = patient.telefono
		formPatient.fields['numexp'].initial = patient.numexp
		formPatient.fields['foto'].initial = patient.foto
		formPatient.fields['activo'].initial = patient.activo
		formPatient.fields['rfc'].initial = patient.rfc
		formPatient.fields['fechaAlta'].initial = patient.fechaAlta
		formPatient.fields['sexo'].initial = patient.sexo
		formPatient.fields['ocupacion'].initial = patient.ocupacion
		formPatient.fields['fechaNacimiento'].initial = patient.fechaNacimiento
		formPatient.fields['fechaUpdate'].initial = patient.fechaUpdate
		return formPatient
	else:
		return None


def filterByIdPatientAdress(idPatient, formAdress):
	printLogQuery("Id recibido for address: "+str(idPatient))
	user = getUser()
	try:
		adress = Adress.objects.get(patient__pk=idPatient, userId=user.id)
		if adress:
			printLogQuery("Address encontrado: {}".format(adress.calle))
			formAdress.fields['calle'].initial = adress.calle
			formAdress.fields['numeroInt'].initial = adress.numeroInt
			formAdress.fields['numeroExt'].initial = adress.numeroExt
			formAdress.fields['ciudad'].initial = adress.ciudad
			formAdress.fields['estado'].initial = adress.estado
			formAdress.fields['cp'].initial = adress.cp
			return formAdress
		else:
			return None
	except Exception as ex:
		log.error("Error: "+str(ex))
		return None


def filterByIdTask(idTask, formTask):
	printLogQuery("Id recibido for task: "+str(idTask))
	user = getUser()
	task = Task.objects.get(pk=idTask, userId=user.id)
	if task:
		log.info("Task encontrado: {}".format(task.nameTask))
		formTask.fields['nameTask'].initial = task.nameTask
		formTask.fields['descTask'].initial = task.descTask
		formTask.fields['status'].initial = task.status
		formTask.fields['dateCreate'].initial = task.dateCreate
		formTask.fields['dateExecute'].initial = task.dateExecute
		return formTask
	else:
		return None

def generateKlave():
	klave = 'P'+date.today().strftime('%d%m%y')+'-'+uuid.uuid4().hex[:5].upper()
	log.info("La clave generada para el paciente es: "+str(klave))
	return klave

def filterPatientDelete(idPatient):
	printLogQuery("Id recibido for patient: "+str(idPatient))
	user = getUser()
	patient = Patient.objects.get(pk=idPatient, userId=user.id)
	if patient:
		return patient
	else:
		return None


def printLogQuery(register):
	log.debug(register)