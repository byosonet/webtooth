from django.apps import AppConfig


class ApppropertiesConfig(AppConfig):
    name = 'appproperties'
    verbose_name = 'Gestión de Propiedades'

    def ready(self):
        from webtooth import signals