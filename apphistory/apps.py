from django.apps import AppConfig


class ApphistoryConfig(AppConfig):
    name = 'apphistory'
    verbose_name = 'Gestión de Historial'

    def ready(self):
        from webtooth import signals