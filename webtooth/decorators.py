from webtooth.config import loadPropertie, createFirstOnly
import logging

from webtooth.config import currentLocalTimestamp
from django.shortcuts import render
from webtooth.settings import MAX_TIME_MINUTES_SESSION
from apppatients.signals import getUser

log = logging.getLogger('apppatients.decorators')
def validRequest(viewReceived):
    def validRequestInternal(request, *args, **kwargs):
        if not process_request(request):
            log.info("Ha vencido la sesión")
       	    data = {"timeModal": 500}
            return render(request, 'home/home.html', data)
        try:
            user = getUser()
            loadPropertie(user.id,request)
        except Exception as ex:
            log.error("Error load propertie: "+str(ex))
            createFirstOnly(request)
        log.info("Load decorators for var sessions in request")
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
        log.info("Last_session: {} Now: {}".format(last_session,now))
        dt = now - last_session

        minutes = int(dt/60)

        log.info("Minutos transcurridos {} desde la última petición".format(minutes))
        if minutes >= MAX_TIME_MINUTES_SESSION:
            log.info("Sesión terminada, se ha excedido el máximo tiempo de espera que es de {} minutos".format(MAX_TIME_MINUTES_SESSION))
            session = False
        else:
            log.info("Sesión vigente, se actualiza el timestamp")
            request.session['last_session'] = now
    except Exception as ex:
        session = False
        log.error("Faltan variables de sesión: {}, se redirige al login".format(ex))
    return session

