from webtooth.config import loadPropertie, createFirstOnly
import logging

from webtooth.config import currentLocalTimestamp
from datetime import datetime
from django.shortcuts import render
from webtooth.settings import MAX_TIME_MINUTES_SESSION, SESSION_EXPIRY_SECONDS
from webtooth.signals import getUser

log = logging.getLogger('webtooth.decorators')
def validRequest(viewReceived):
    def validRequestInternal(request, *args, **kwargs):
        if not process_request(request):
            log.info("Ha vencido la sesión")
       	    data = {"timeModal": 500}
            return render(request, 'home/home.html', data)
        try:
            user = getUser()
            loadPropertie(user.id,request)            
            request.session.set_expiry(SESSION_EXPIRY_SECONDS)
        except Exception as ex:
            log.error("Error load propertie: "+str(ex))
            createFirstOnly(request)
        printLogDecorators("Load decorators for var sessions in request")
        return viewReceived(request, *args, **kwargs)
    return validRequestInternal


def process_request(request):
    session = True
    try:
        found = False
        for key in request.session.keys():
            if key == 'last_session':
                found = True
                break
        if not found:
            request.session['last_session'] = currentLocalTimestamp()

        last_session = request.session['last_session']
        now = currentLocalTimestamp()
        last = datetime.fromtimestamp(last_session)
        last_format = last.strftime("%d/%m/%Y %H:%M:%S %p")       
        now_today = datetime.fromtimestamp(now)
        now_format = now_today.strftime("%d/%m/%Y %H:%M:%S %p")
        log.info(">>> Last_request: {} >>> Now_request: {}".format(last_format,now_format))
        dt = now - last_session

        minutes = int(dt/60)

        log.info(">>> {} Minutos transcurridos desde la última petición".format(minutes))
        if minutes >= MAX_TIME_MINUTES_SESSION:
            log.info("Sesión terminada, se ha excedido el máximo tiempo de espera que es de {} minutos".format(MAX_TIME_MINUTES_SESSION))
            session = False
        else:
            log.info("Sesión vigente")
            request.session['last_session'] = now
    except Exception as ex:
        session = False
        log.error("Faltan variables de sesión: {}, se redirige al login".format(ex))
    return session

def printLogDecorators(register):
    log.debug(register)