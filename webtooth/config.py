import logging
import shutil

from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from apppatients.models import Propertie, Task
from apppatients.signals import getUser

from webtooth.logger import LOGGING
from webtooth.settings import PATH_LOGS, PATH_ZIPMAIL
from django.db import connection
from django.db.models import Q

#Service logger
def logger(app,view):
	logging.config.dictConfig(LOGGING)
	if view:
		log = logging.getLogger(str(app)+'.views')
	else:
		log = logging.getLogger(str(app))
	return log

log = logger('config',False)

#Redirect al login de la aplicacion
def getLogin():
	return '/admin/login/'

#Service sendEmailContact
def sendEmailContact(dataContact):
	user = getUser()
	subject = dataContact['subjectRecipe']
	email = dataContact['emailRecipe']
	message = "Hola " + dataContact['nameRecipe'].title() + ", aquí tienes tu receta: \n\n" + \
            dataContact['descRecipe'] + "\n\n¡Gracias por tu preferencia!, favor de no responder este correo.\n\nAtte.\n"+user.get_full_name()
	email_from =  settings.EMAIL_HOST_USER
	email_to = settings.EMAIL_TO
	email_to.append(email)
	try:
		log.info("Enviando correo...TO: "+str(email_to))
		log.info("Enviando correo...CC: "+str(settings.EMAIL_CC))
		log.info("Enviando correo...BCC: "+str(settings.EMAIL_BCC))
		emailMessage = EmailMessage(subject, message, email_from, email_to, cc=settings.EMAIL_CC, bcc=settings.EMAIL_BCC)
		emailMessage.send()
		log.info("Correo enviado correctamente...TO "+str(email_to))
		log.info("Correo enviado correctamente...CC"+str(settings.EMAIL_CC))
		log.info("Correo enviado correctamente...BCC"+str(settings.EMAIL_BCC))
		return email
	except Exception as ex:
		log.error("Error al enviar correo: "+str(ex))
		return None

def getAllLoggedUsers():
    sessions = Session.objects.filter(expire_date__gte=currentLocalTime())
    uid_list = []
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id'))
    return User.objects.filter(id__in=uid_list).count()

def createPropertie(userId, k, v):
	prop = Propertie.objects.filter(key=k, userId=userId)
	if not prop:
		Propertie.objects.create(userId=userId, key=k, value=v)


def updatePropertie(userId, k, v):
	prop = Propertie.objects.get(key=k, userId=userId)
	prop.value = v
	prop.save()

def loadPropertie(userId, request):
	bg = Propertie.objects.get(key='bg_color', userId=userId)
	bt = Propertie.objects.get(key='bt_color', userId=userId)
	fg = Propertie.objects.get(key='fg_color', userId=userId)
	ad = Propertie.objects.get(key='ad_color', userId=userId)
	lr = Propertie.objects.get(key='last_row', userId=userId)
	cm = Propertie.objects.get(key='class_menu', userId=userId)
	request.session[bg.key] = bg.value
	request.session[bt.key] = bt.value
	request.session[fg.key] = fg.value
	request.session[ad.key] = ad.value
	request.session[lr.key] = lr.value
	request.session[cm.key] = cm.value
	printLogConfig("{}, {}, {}".format(bg,bt,fg))

def createFirstOnly(request):	
	createPropertie(userRequest(), 'bg_color','gradient-primary')
	createPropertie(userRequest(), 'fg_color', 'white')
	createPropertie(userRequest(),'bt_color', 'primary')
	createPropertie(userRequest(),'ad_color', '#4e73df')
	createPropertie(userRequest(), 'last_row', str(0))
	createPropertie(userRequest(),'class_menu', '')

def setColorSystem(request,idColor):
	log.info("Cambiando el color al sistema, idColor recibido: {}".format(idColor))	
	if idColor == 1:
		updatePropertie(userRequest(),'bg_color', 'gradient-dark')
		updatePropertie(userRequest(),'bt_color', 'dark')
		updatePropertie(userRequest(),'fg_color', 'white')
		updatePropertie(userRequest(),'ad_color', '#5a5c69')
		loadPropertie(userRequest(), request)

		log.info("Cambiando color de tema a negro")
	elif idColor == 2:
		updatePropertie(userRequest(), 'bg_color', 'gradient-success')
		updatePropertie(userRequest(), 'bt_color', 'success')
		updatePropertie(userRequest(), 'fg_color', 'white')
		updatePropertie(userRequest(), 'ad_color', '#1cc88a')
		loadPropertie(userRequest(), request)

		log.info("Cambiando color de tema a verde")
	elif idColor == 3:
		updatePropertie(userRequest(),'bg_color', 'gradient-light')
		updatePropertie(userRequest(),'bt_color', 'secondary')
		updatePropertie(userRequest(),'fg_color', 'dark')
		updatePropertie(userRequest(), 'ad_color', '#858796')
		loadPropertie(userRequest(), request)

		log.info("Cambiando color de tema a Blanco")
	elif idColor == 4:
		updatePropertie(userRequest(),'bg_color', 'gradient-secondary')
		updatePropertie(userRequest(),'bt_color', 'secondary')
		updatePropertie(userRequest(),'fg_color', 'white')
		updatePropertie(userRequest(),'ad_color', '#858796')
		loadPropertie(userRequest(), request)

		log.info("Cambiando color de tema a gris")
	elif idColor == 5:
		updatePropertie(userRequest(),'bg_color', 'gradient-danger')
		updatePropertie(userRequest(), 'bt_color', 'danger')
		updatePropertie(userRequest(),'fg_color', 'white')
		updatePropertie(userRequest(), 'ad_color', '#e74a3b')
		loadPropertie(userRequest(), request)

		log.info("Cambiando color de tema a rojo")
	elif idColor == 6:
		updatePropertie(userRequest(),'bg_color', 'gradient-warning')
		updatePropertie(userRequest(),'bt_color', 'warning')
		updatePropertie(userRequest(),'fg_color', 'dark')
		updatePropertie(userRequest(), 'ad_color', '#f6c23e')
		loadPropertie(userRequest(), request)

		log.info("Cambiando color de tema a naranja")
	elif idColor == 7:
		updatePropertie(userRequest(),'bg_color', 'gradient-primary')
		updatePropertie(userRequest(),'bt_color', 'primary')
		updatePropertie(userRequest(),'fg_color', 'white')
		updatePropertie(userRequest(), 'ad_color', '#4e73df')
		loadPropertie(userRequest(), request)

		log.info("Cambiando color de tema a Default")
	request.session['color_default'] = True
	return request


def getListTask(request, user):
	today = str(currentLocalDate()).split('-')
	if user == 'admin':
		listTask = Task.objects.filter(			
			status=False,
			dateExecute=None,
			dateCreate__year=today[0],
			dateCreate__month=today[1],
			dateCreate__day=today[2]).order_by('-dateCreate')
	else:
		listTask = Task.objects.filter(
			userCode=user,
			status=False,
			dateExecute=None,
			dateCreate__year=today[0],
			dateCreate__month=today[1],
			dateCreate__day=today[2]).order_by('-dateCreate')

	if listTask and len(listTask) > 0:
		data = {}
		for item in listTask:
			log.debug("Load item "+str(item))
			data[item.id] = item.nameTask
		request.session['dataTask'] = data
		request.session['countTask'] = len(listTask)
	else:
		request.session['dataTask'] = None
		request.session['countTask'] = 0


def getListTaskHome(user):
	today = str(currentLocalDate()).split('-')

	if user == 'admin':
		listTaskHome = Task.objects.filter(
			status=True,
			dateExecute__year=today[0],
			dateExecute__month=today[1],
			dateExecute__day=today[2]).order_by('-dateExecute')
	else:
		listTaskHome = Task.objects.filter(
			userCode=user,
			status=True,
			dateExecute__year=today[0],
			dateExecute__month=today[1],
			dateExecute__day=today[2]).order_by('-dateExecute')

	if listTaskHome and len(listTaskHome) > 0:
		for item in listTaskHome:
			printLogConfig("Load task home "+str(item))
		return listTaskHome
	else:
		return None

def compressLogsZip():
	today = str('webtooth-logs-')+str(currentLocalDate())
	shutil.make_archive(PATH_ZIPMAIL+today, 'zip',PATH_LOGS)
	ficheroGenerado = str(today+'.zip')
	log.info("Logs comprimidos con exito, fichero generado: " + ficheroGenerado)
	return ficheroGenerado

def sendEmailLogs():	
	fileZip = compressLogsZip()
	today = str(currentLocalDate())
	subject = 'Logs del sistema Webtooth - '+today
	message = "Se envía los ficheros logs de la plataforma Webtooth lanzado por el cron del sistema."
	email_from = settings.EMAIL_HOST_USER
	email_to = settings.EMAIL_HOST_SUPPORT
	
	try:
		log.info("Enviando correo a soporte: "+str(email_to))

		emailSupport = EmailMessage(subject, message, email_from, email_to)
		emailSupport.attach_file(PATH_ZIPMAIL+str(fileZip))
		emailSupport.send()

		log.info("Correo enviado correctamente a: "+str(email_to))
	except Exception as ex:
		log.error("Error al enviar correo a soporte: "+str(ex))

def currentLocalDate():
	date = timezone.localtime(timezone.now()).date()
	printLogConfig("Return value date now: "+str(date))
	return date


def currentLocalTime():
	time = timezone.localtime(timezone.now())
	printLogConfig("Return value time now: "+str(time))
	return time


def currentLocalTimestamp():
	timestamp = timezone.localtime(timezone.now()).timestamp()
	printLogConfig("Return value timestamp now: "+str(timestamp))
	return timestamp

def printLogConfig(register):
	log.debug(register)

def userRequest():
    user = getUser()
    return user.id

def filterQuery():
	user = getUser()
	if user.get_username() == 'admin':
		customQuery = Q()
	else:
		customQuery = Q(userId=user.id)
	return customQuery