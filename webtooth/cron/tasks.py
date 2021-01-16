from datetime import datetime
from webtooth.config import logger

log = logger('appGestionPacientes.config', False)

def logMailTask():
    log.info("Task execute logMailTask now: "+str(datetime.now()))


def monitorTask():
    log.info("Task execute monitorTask now: "+str(datetime.now()))