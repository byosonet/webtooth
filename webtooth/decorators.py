from webtooth.config import loadPropertie
import logging

from django.utils import timezone
from django.shortcuts import render
from webtooth.settings import MAX_TIME_MINUTES_SESSION

log = logging.getLogger('appGestionPacientes.decorators')
def validRequest(viewReceived):
    def validRequestInternal(request, *args, **kwargs):
        if not process_request(request):
            log.info("Ha vencido la sesión")
       	    data = {"timeModal": 500}
            return render(request, 'other/session.html', data)
        loadPropertie(request)
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
            request.session['last_session'] = timezone.now().timestamp()

        last_session = request.session['last_session']
        now = timezone.now().timestamp()
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

