from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from webtooth.cron import tasks


def logMailTimer():
    cron = BackgroundScheduler()
    cron.add_job(tasks.logMailTask, 'cron', hour=20, minute=15, id="jobLogMailTimer")
    cron.start()


def monitorTimer():
    cron = BackgroundScheduler()
    cron.add_job(tasks.monitorTask, 'interval', seconds=5, id="jobMonitorTimer")
    cron.start()
