from django.apps import AppConfig


class ApppatientsConfig(AppConfig):
    name = 'apppatients'
    verbose_name = 'Gestión de Pacientes'

    def ready(self):
        from webtooth import signals
