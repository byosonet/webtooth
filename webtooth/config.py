import logging
import shutil

from django.core.mail import send_mail, EmailMessage
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from appGestionPacientes.models import Propertie, Task
from appGestionPacientes.signals import getUser

from webtooth.logger import LOGGING
from webtooth.settings import PATH_LOGS, PATH_ZIPMAIL, EMAIL_HOST_SUPPORT

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
	subject = dataContact['subjectRecipe']
	email = dataContact['emailRecipe']
	message = "Hola " + dataContact['nameRecipe'].title() + ", aquí tienes tu receta: \n\n" + \
            dataContact['descRecipe'] + "\n\n¡Gracias por tu preferencia!"
	email_from =  settings.EMAIL_HOST_USER
	email_to = settings.EMAIL_TO
	email_to.append(email)
	try:
		log.info("Enviando correo...a: "+str(email_to))
		send_mail(subject, message, email_from, email_to)
		log.info("Correo enviado correctamente a: "+str(email_to))
		return email
	except Exception as ex:
		log.error("Error al enviar correo: "+str(ex))
		return None

def getAllLoggedUsers():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
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
	request.session[bg.key] = bg.value
	request.session[bt.key] = bt.value
	request.session[fg.key] = fg.value
	request.session[ad.key] = ad.value
	request.session[lr.key] = lr.value
	log.info("{}, {}, {}".format(bg,bt,fg))

def createFirstOnly(request):
	user = getUser()
	createPropertie(user.id, 'bg_color','gradient-primary')
	createPropertie(user.id, 'fg_color', 'white')
	createPropertie(user.id,'bt_color', 'primary')
	createPropertie(user.id,'ad_color', '#4e73df')
	createPropertie(user.id, 'last_row', str(0))

def setColorSystem(request,idColor):
	log.info("Cambiando el color al sistema, idColor recibido: {}".format(idColor))
	user = getUser()
	if idColor == 1:
		updatePropertie(user.id,'bg_color', 'gradient-dark')
		updatePropertie(user.id,'bt_color', 'dark')
		updatePropertie(user.id,'fg_color', 'white')
		updatePropertie(user.id,'ad_color', '#5a5c69')
		loadPropertie(user.id, request)

		log.info("Cambiando color de tema a negro")
	elif idColor == 2:
		updatePropertie(user.id, 'bg_color', 'gradient-success')
		updatePropertie(user.id, 'bt_color', 'success')
		updatePropertie(user.id, 'fg_color', 'white')
		updatePropertie(user.id, 'ad_color', '#1cc88a')
		loadPropertie(user.id, request)

		log.info("Cambiando color de tema a verde")
	elif idColor == 3:
		updatePropertie(user.id,'bg_color', 'gradient-light')
		updatePropertie(user.id,'bt_color', 'secondary')
		updatePropertie(user.id,'fg_color', 'dark')
		updatePropertie(user.id, 'ad_color', '#858796')
		loadPropertie(user.id, request)

		log.info("Cambiando color de tema a Blanco")
	elif idColor == 4:
		updatePropertie(user.id,'bg_color', 'gradient-secondary')
		updatePropertie(user.id,'bt_color', 'secondary')
		updatePropertie(user.id,'fg_color', 'white')
		updatePropertie(user.id,'ad_color', '#858796')
		loadPropertie(user.id, request)

		log.info("Cambiando color de tema a gris")
	elif idColor == 5:
		updatePropertie(user.id,'bg_color', 'gradient-danger')
		updatePropertie(user.id, 'bt_color', 'danger')
		updatePropertie(user.id,'fg_color', 'white')
		updatePropertie(user.id, 'ad_color', '#e74a3b')
		loadPropertie(user.id, request)

		log.info("Cambiando color de tema a rojo")
	elif idColor == 6:
		updatePropertie(user.id,'bg_color', 'gradient-warning')
		updatePropertie(user.id,'bt_color', 'warning')
		updatePropertie(user.id,'fg_color', 'dark')
		updatePropertie(user.id, 'ad_color', '#f6c23e')
		loadPropertie(user.id, request)

		log.info("Cambiando color de tema a naranja")
	elif idColor == 7:
		updatePropertie(user.id,'bg_color', 'gradient-primary')
		updatePropertie(user.id,'bt_color', 'primary')
		updatePropertie(user.id,'fg_color', 'white')
		updatePropertie(user.id, 'ad_color', '#4e73df')
		loadPropertie(user.id, request)

		log.info("Cambiando color de tema a Default")
	request.session['color_default'] = True
	return request


def getListTask(request, user):

	today = str(timezone.now().date()).split('-')
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
			log.info("Load item "+str(item))
			data[item.id] = item.nameTask
		request.session['dataTask'] = data
		request.session['countTask'] = len(listTask)
	else:
		request.session['dataTask'] = None
		request.session['countTask'] = 0


def getListTaskHome(user):
	today = str(timezone.now().date()).split('-')
	listTaskHome = Task.objects.filter(
		userCode=user,
		status=True,
		dateExecute__year=today[0],
		dateExecute__month=today[1],
		dateExecute__day=today[2]).order_by('-dateExecute')

	if listTaskHome and len(listTaskHome) > 0:
		for item in listTaskHome:
			log.info("Load task home "+str(item))
		return listTaskHome
	else:
		return None

def compressLogsZip():
	today = str('webtooth-logs-')+str(timezone.now().date())
	shutil.make_archive(PATH_ZIPMAIL+today, 'zip',PATH_LOGS)
	ficheroGenerado = str(today+'.zip')
	log.info("Logs comprimidos con exito, fichero generado: " + ficheroGenerado)
	return ficheroGenerado

def sendEmailLogs():	
	fileZip = compressLogsZip()
	today = str(timezone.now().date())
	subject = 'Logs comprimidos del sistema Webtooth - '+today
	email = EMAIL_HOST_SUPPORT
	message = "Se envía los ficheros logs de la plataforma Webtooth lanzado por el cron del sistema."
	email_from = settings.EMAIL_HOST_USER
	email_to = settings.EMAIL_TO
	email_to.append(email)
	try:
		log.info("Enviando correo a soporte: "+str(email_to))

		emailSupport = EmailMessage(subject, message, email_from, email_to)
		emailSupport.attach_file(PATH_ZIPMAIL+str(fileZip))
		emailSupport.send()

		log.info("Correo enviado correctamente a: "+str(email_to))
	except Exception as ex:
		log.error("Error al enviar correo a soporte: "+str(ex))
