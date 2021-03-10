from datetime import datetime
from webtooth.config import logger, sendEmailLogs

log = logger('tasks.config', False)
FORMAT_TIME = "%d/%m/%Y %H:%M:%S %p"

def logMailTask():
    now_today = datetime.now()
    now_format = now_today.strftime(FORMAT_TIME)
    log.info("Task execute logMailTask now: "+str(now_format))
    sendEmailLogs()


def monitorTask():
    now_today = datetime.now()
    now_format = now_today.strftime(FORMAT_TIME)
    log.info("Task execute monitorTask now: "+str(now_format))
