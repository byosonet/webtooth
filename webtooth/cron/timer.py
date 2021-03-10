from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from webtooth.cron import tasks
from django.conf import settings


def logMailTimer():
    if settings.JOBLOGMAILTIMER:
        cron = BackgroundScheduler()
        cron.add_job(tasks.logMailTask, 'cron', hour=18, minute=21, id="jobLogMailTimer")
        cron.start()


def monitorTimer():
    if settings.JOBMONITORTIMER:
        cron = BackgroundScheduler()
        cron.add_job(tasks.monitorTask, 'interval', seconds=5, id="jobMonitorTimer")
        cron.start()
