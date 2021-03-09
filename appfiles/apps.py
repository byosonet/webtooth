from django.apps import AppConfig


class AppfilesConfig(AppConfig):
    name = 'appfiles'
    verbose_name = 'Gestión de Archivos'

    def ready(self):
        from webtooth import signals
