import logging

from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from appGestionPacientes.models import Propertie


#Service logger
def logger(app,view):
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
	subject=dataContact['asunto']
	email=dataContact['email']
	message = "Hola " + dataContact['nombre'].title() + ", aquí tienes tu receta: \n\n" + \
            dataContact['mensaje'] + "\n\n¡Gracias por tu preferencia!"
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

def createPropertie(k,v):
	prop = Propertie.objects.filter(key=k)
	if not prop:
		Propertie.objects.create(key=k, value=v)

def updatePropertie(k, v):
	prop = Propertie.objects.get(key=k)
	prop.value = v
	prop.save()

def loadPropertie(request):
	bg = Propertie.objects.get(key='bg_color')
	bt = Propertie.objects.get(key='bt_color')
	fg = Propertie.objects.get(key='fg_color')
	ad = Propertie.objects.get(key='ad_color')
	lr = Propertie.objects.get(key='last_row')
	request.session[bg.key] = bg.value
	request.session[bt.key] = bt.value
	request.session[fg.key] = fg.value
	request.session[ad.key] = ad.value
	request.session[lr.key] = lr.value
	log.info("{}, {}, {}".format(bg,bt,fg))

def createFirstOnly(request):
	createPropertie('bg_color','gradient-primary')
	createPropertie('fg_color', 'white')
	createPropertie('bt_color', 'primary')
	createPropertie('ad_color', '#4e73df')
	createPropertie('last_row', str(0))

def setColorSystem(request,idColor):
	log.info("Cambiando el color al sistema, idColor recibido: {}".format(idColor))
	if idColor == 1:
		updatePropertie('bg_color','gradient-dark')
		updatePropertie('bt_color', 'dark')
		updatePropertie('fg_color', 'white')
		updatePropertie('ad_color', '#5a5c69')
		loadPropertie(request)

		log.info("Cambiando color de tema a negro")
	elif idColor == 2:
		updatePropertie('bg_color', 'gradient-success')
		updatePropertie('bt_color', 'success')
		updatePropertie('fg_color', 'white')
		updatePropertie('ad_color', '#1cc88a')
		loadPropertie(request)

		log.info("Cambiando color de tema a verde")
	elif idColor == 3:
		updatePropertie('bg_color', 'gradient-light')
		updatePropertie('bt_color', 'secondary')
		updatePropertie('fg_color', 'dark')
		updatePropertie('ad_color', '#858796')
		loadPropertie(request)

		log.info("Cambiando color de tema a Blanco")
	elif idColor == 4:
		updatePropertie('bg_color', 'gradient-secondary')
		updatePropertie('bt_color', 'secondary')
		updatePropertie('fg_color', 'white')
		updatePropertie('ad_color', '#858796')
		loadPropertie(request)

		log.info("Cambiando color de tema a gris")
	elif idColor == 5:
		updatePropertie('bg_color', 'gradient-danger')
		updatePropertie('bt_color', 'danger')
		updatePropertie('fg_color', 'white')
		updatePropertie('ad_color', '#e74a3b')
		loadPropertie(request)

		log.info("Cambiando color de tema a rojo")
	elif idColor == 6:
		updatePropertie('bg_color', 'gradient-warning')
		updatePropertie('bt_color', 'warning')
		updatePropertie('fg_color', 'dark')
		updatePropertie('ad_color', '#f6c23e')
		loadPropertie(request)

		log.info("Cambiando color de tema a naranja")
	elif idColor == 7:
		updatePropertie('bg_color', 'gradient-primary')
		updatePropertie('bt_color', 'primary')
		updatePropertie('fg_color', 'white')
		updatePropertie('ad_color', '#4e73df')
		loadPropertie(request)

		log.info("Cambiando color de tema a Default")
	request.session['color_default'] = True
	return request
