from django.apps import AppConfig


class AppadminConfig(AppConfig):
    name = 'appadmin'
    verbose_name = 'Gestión de Administración'

    def ready(self):
        from . cron import timer
        timer.logMailTimer()
        timer.monitorTimer()