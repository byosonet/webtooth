from django.apps import AppConfig

class AppnavigationsConfig(AppConfig):
    name = 'appnavigations'
    verbose_name = 'Gestión de Navegación'

    def ready(self):
        from webtooth import signals