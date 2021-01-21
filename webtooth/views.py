from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from webtooth.config import getLogin, getListTask, getListTaskHome
from webtooth.config import logger,getAllLoggedUsers
from webtooth.config import setColorSystem, createPropertie, loadPropertie, updatePropertie

from appGestionPacientes.models import Patient, File

from django.db.models import Q
from webtooth.decorators import validRequest
from django.utils import timezone

from appGestionPacientes.signals import getUser

import os, shutil
from django.conf import settings

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
	getListTask(request, user.get_username())
	listadoTareasHome = getListTaskHome(user.get_username())
	log.info("LastRow: {}".format(lastRow))	
	createPropertie(user.id, 'last_row', str(lastRow))
	request.session['last_session'] = timezone.now().timestamp()
	rowsRegister=Patient.objects.all().count()
	rowsFile = File.objects.all().count()
	loggedUsers = getAllLoggedUsers()
	patientActive = Patient.objects.filter(Q(eliminado=None) | Q(eliminado=False), activo=True).count()
	patientInactive = Patient.objects.filter(Q(eliminado=None) | Q(eliminado=False),Q(activo=False) | Q(activo=None)).count()
	patientDelete = Patient.objects.filter(eliminado=True).count()

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

	log.info("Total de pacientes Activos: {}".format(patientActive))
	log.info("Total de pacientes Inactivos: {}".format(patientInactive))
	log.info("Total de pacientes Eliminados: {}".format(patientDelete))
	log.info("Total de pacientes en Sistema: {}".format(rowsRegister))
	log.info("Porcentaje de activos: {}%".format(porcentajeActivos))
	log.info("Porcentaje de Inactivos: {}%".format(porcentajeInactivos))
	log.info("Porcentaje de Eliminados: {}%".format(porcentajeEliminados))
	infoDisk(request)
	infoDiskUpload(request)
	data = {"rowsFile": rowsFile, "rowsRegister": rowsRegister, "loggedUsers": loggedUsers,
         "percentActive": porcentajeActivos, "percentInactive": porcentajeInactivos, 
         "patientActive": patientActive, "inactivePatients": patientInactive, "lastRow": lastRow, "patientDelete": patientDelete, "porcentajeEliminados": porcentajeEliminados, 
		 "listadoTareasHome": listadoTareasHome}
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
	log.info("Total disk space: %d Gb" % totalDisk)
	
	usedDisk = (used // (2**30))
	log.info("Total used disk space: %d Gb" % usedDisk)

	freeDisk = (free // (2**30))
	log.info("Total free disk space: %d Gb" % freeDisk)

	porcentajeUsado = (usedDisk * 100)/totalDisk
	porcentajeUsado = format(porcentajeUsado, '.2f')

	porcentajeLibre = (freeDisk * 100)/totalDisk
	porcentajeLibre = format(porcentajeLibre, '.2f')

	request.session['total_disk_gb'] = totalDisk
	request.session['used_disk_gb'] = usedDisk
	request.session['free_disk_gb'] = freeDisk

	request.session['used_disk'] = porcentajeUsado
	request.session['free_disk'] = porcentajeLibre

	log.info("Porcentaje de disco usado: {}%".format(porcentajeUsado))
	log.info("Porcentaje de disco libre: {}%".format(porcentajeLibre))


def infoDiskUpload(request):
	total = folderSizeMB(settings.MEDIA_PATH+str('upload'))
	totalDisk = (total // (1024)) / 1024
	totalDisk = format(totalDisk, '.2f')
	log.info("Total disk upload: {} Mb".format(totalDisk))
	request.session['used_disk_up'] = totalDisk


def folderSizeMB(path):
    total = 0
    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += folderSizeMB(entry.path)
    return total
