from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from . import tasks
from django.conf import settings


def logMailTimer():
    if settings.JOBLOGMAILTIMER:
        cron = BackgroundScheduler(timezone=settings.TIME_ZONE)
        cron.add_job(tasks.logMailTask, 'cron', hour='17', minute='15', id="jobLogMailTimer")
        cron.start()


def monitorTimer():
    if settings.JOBMONITORTIMER:
        cron = BackgroundScheduler(timezone=settings.TIME_ZONE)
        cron.add_job(tasks.monitorTask, 'interval', seconds=5, id="jobMonitorTimer")
        cron.start()
