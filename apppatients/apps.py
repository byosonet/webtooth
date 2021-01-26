from django.apps import AppConfig


class ApppatientsConfig(AppConfig):
    name = 'apppatients'
    verbose_name = 'Gestión de Pacientes'

    def ready(self):
        from apppatients import signals
        from webtooth.cron import timer
        timer.logMailTimer()
        timer.monitorTimer()
