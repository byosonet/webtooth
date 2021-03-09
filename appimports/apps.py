from django.apps import AppConfig


class AppimportsConfig(AppConfig):
    name = 'appimports'
    verbose_name = 'Gestión de Importaciones'

    def ready(self):
        from webtooth import signals