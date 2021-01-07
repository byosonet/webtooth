from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from webtooth.config import getLogin
from webtooth.config import logger,getAllLoggedUsers
from webtooth.config import setColorSystem, createPropertie, loadPropertie, updatePropertie

from appGestionPacientes.models import Patient, File

from django.db.models import Q
from webtooth.decorators import validRequest
from django.utils import timezone

from appGestionPacientes.signals import getUser


log = logger('webtooth',True)

@login_required(login_url=getLogin())
@validRequest
def homeView(request):	
	lastRow = 0
	user = getUser()
	try:
		lastRow = Patient.objects.all().order_by('-fechaUpdate')[0].id
		updatePropertie(user.id,'last_row', str(lastRow))
	except Exception:
		pass
	log.info("LastRow: {}".format(lastRow))	
	createPropertie(user.id, 'last_row', str(lastRow))
	request.session['last_session'] = timezone.now().timestamp()
	rowsRegister=Patient.objects.all().count()
	rowsFile = File.objects.all().count()
	loggedUsers = getAllLoggedUsers()
	patientActive = Patient.objects.filter(activo=True).count()
	patientInactive = Patient.objects.filter(Q(activo=False) | Q(activo=None)).count()

	if rowsRegister > 0 :
		porcentajeActivos = (patientActive * 100)/rowsRegister
		porcentajeActivos = format(porcentajeActivos,'.2f')

		porcentajeInactivos = (patientInactive * 100)/rowsRegister
		porcentajeInactivos = format(porcentajeInactivos, '.2f')
	else:
		porcentajeActivos = 0
		porcentajeInactivos = 0

	try:
		loadPropertie(user.id, request)
		log.info("El sistema ya tiene color activado")
	except Exception as ex:
		log.error("Error: "+str(ex))
		log.info("El sistema no tiene color de tema, cargando por default.")		
		createPropertie(user.id,'bg_color','gradient-primary')
		createPropertie(user.id,'fg_color', 'white')
		createPropertie(user.id,'bt_color', 'primary')
		createPropertie(user.id,'ad_color', '#4e73df')
		loadPropertie(user.id, request)
		log.info("Se ha cargado color de tema por default")

	log.info("Total de pacientes Activos: {}".format(patientActive))
	log.info("Total de pacientes Inactivos: {}".format(patientInactive))
	log.info("Porcentaje de activos: {}%".format(porcentajeActivos))
	log.info("Porcentaje de Inactivos: {}%".format(porcentajeInactivos))
	data = {"rowsFile": rowsFile, "rowsRegister": rowsRegister, "loggedUsers": loggedUsers,
         "percentActive": porcentajeActivos, "percentInactive": porcentajeInactivos, 
         "patientActive": patientActive, "inactivePatients": patientInactive, "lastRow": lastRow}
	return render(request,"home/home.html",data)


@validRequest
def error404(request, exception):
	log.error("Página no encontrada: ")
	message="Lo sentimos, página no encontrada"
	data = {"data":message}
	return render(request,'other/404.html', data)


@validRequest
def notHasPermission(request):
	log.error("El usuario no tiene los permisos suficientes para acceder a la vista seleccionada")
	return render(request,'other/permission.html')

def color(request,idColor):
	request = setColorSystem(request, idColor)
	return redirect('/')

