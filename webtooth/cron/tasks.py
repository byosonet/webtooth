from datetime import datetime
from webtooth.config import logger, sendEmailLogs

log = logger('apppatients.config', False)

def logMailTask():
    log.info("Task execute logMailTask now: "+str(datetime.now()))
    sendEmailLogs()


def monitorTask():
    log.info("Task execute monitorTask now: "+str(datetime.now()))
