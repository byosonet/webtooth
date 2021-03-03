from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from webtooth.config import getLogin, getListTask, getListTaskHome
from webtooth.config import logger,getAllLoggedUsers
from webtooth.config import setColorSystem, createPropertie, loadPropertie, updatePropertie

from apppatients.models import Patient, File, Task, Recipe

from django.db.models import Q
from webtooth.decorators import validRequest
from webtooth.config import currentLocalTimestamp

from apppatients.signals import getUser

import os, shutil
from django.conf import settings

log = logger('webtooth',True)

@login_required(login_url=getLogin())
@validRequest
def homeView(request):	
	lastRow = 0
	user = getUser()
	try:
		lastRow = Patient.objects.filter(userId=user.id).order_by('-fechaUpdate')[0].id
		updatePropertie(user.id,'last_row', str(lastRow))
	except Exception:
		pass
	getListTask(request, user.get_username())
	listadoTareasHome = getListTaskHome(user.get_username())
	printLogHome("LastRow: {}".format(lastRow))	
	createPropertie(user.id, 'last_row', str(lastRow))
	request.session['last_session'] = currentLocalTimestamp()
	rowsRegister=Patient.objects.filter(userId=user.id).count()
	rowsFile = File.objects.filter(userId=user.id).count()
	taskEje = Task.objects.filter(status=True, userId=user.id).count()
	recipeSend = Recipe.objects.filter(userId=user.id, stateRecipe='Enviado').count()
	loggedUsers = getAllLoggedUsers()
	patientActive = Patient.objects.filter(Q(eliminado=None) | Q(eliminado=False), activo=True).filter(userId=user.id).count()
	patientInactive = Patient.objects.filter(Q(eliminado=None) | Q(eliminado=False),Q(activo=False) | Q(activo=None)).filter(userId=user.id).count()
	patientDelete = Patient.objects.filter(eliminado=True).filter(userId=user.id).count()

	if rowsRegister > 0 :
		porcentajeActivos = (patientActive * 100)/rowsRegister
		porcentajeActivos = format(porcentajeActivos,'.2f')

		porcentajeInactivos = (patientInactive * 100)/rowsRegister
		porcentajeInactivos = format(porcentajeInactivos, '.2f')

		porcentajeEliminados = (patientDelete * 100)/rowsRegister
		porcentajeEliminados = format(porcentajeEliminados, '.2f')
	else:
		porcentajeActivos = 0
		porcentajeInactivos = 0
		porcentajeEliminados = 0

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

	printLogHome("Total de pacientes Activos: {}".format(patientActive))
	printLogHome("Total de pacientes Inactivos: {}".format(patientInactive))
	printLogHome("Total de pacientes Eliminados: {}".format(patientDelete))
	printLogHome("Total de pacientes en Sistema: {}".format(rowsRegister))
	printLogHome("Porcentaje de activos: {}%".format(porcentajeActivos))
	printLogHome("Porcentaje de Inactivos: {}%".format(porcentajeInactivos))
	printLogHome("Porcentaje de Eliminados: {}%".format(porcentajeEliminados))
	infoDisk(request)
	infoDiskUpload(request)
	data = {"rowsFile": rowsFile, "rowsRegister": rowsRegister, "loggedUsers": loggedUsers,
         "percentActive": porcentajeActivos, "percentInactive": porcentajeInactivos, 
         "patientActive": patientActive, "inactivePatients": patientInactive, "lastRow": lastRow, "patientDelete": patientDelete, "porcentajeEliminados": porcentajeEliminados, 
         "listadoTareasHome": listadoTareasHome, "taskEje": taskEje, "recipeSend": recipeSend}
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

def infoDisk(request):
	total, used, free = shutil.disk_usage("/")

	totalDisk = (total // (2**30))
	printLogHome("Total disk space: %d Gb" % totalDisk)
	
	usedDisk = (used // (2**30))
	printLogHome("Total used disk space: %d Gb" % usedDisk)

	freeDisk = (free // (2**30))
	printLogHome("Total free disk space: %d Gb" % freeDisk)

	porcentajeUsado = (usedDisk * 100)/totalDisk
	porcentajeUsado = format(porcentajeUsado, '.2f')

	porcentajeLibre = (freeDisk * 100)/totalDisk
	porcentajeLibre = format(porcentajeLibre, '.2f')

	request.session['total_disk_gb'] = totalDisk
	request.session['used_disk_gb'] = usedDisk
	request.session['free_disk_gb'] = freeDisk

	request.session['used_disk'] = porcentajeUsado
	request.session['free_disk'] = porcentajeLibre

	printLogHome("Porcentaje de disco usado: {}%".format(porcentajeUsado))
	printLogHome("Porcentaje de disco libre: {}%".format(porcentajeLibre))


def infoDiskUpload(request):
	total = folderSizeMB(settings.MEDIA_PATH+str('upload'))
	totalDisk = (total // (1024)) / 1024
	totalDisk = format(totalDisk, '.2f')
	printLogHome("Total disk upload: {} Mb".format(totalDisk))
	request.session['used_disk_up'] = totalDisk


def folderSizeMB(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folderSizeMB(entry.path)
    return total

def printLogHome(register):
	log.debug(register)