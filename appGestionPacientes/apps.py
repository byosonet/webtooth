from django.apps import AppConfig


class AppgestionpacientesConfig(AppConfig):
    name = 'appGestionPacientes'
    verbose_name = 'Gestión de Pacientes'

    def ready(self):
        from appGestionPacientes import signals
