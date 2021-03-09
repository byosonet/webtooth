from django.apps import AppConfig


class ApptasksConfig(AppConfig):
    name = 'apptasks'
    verbose_name = 'Gestión de Tareas'

    def ready(self):
        from webtooth import signals