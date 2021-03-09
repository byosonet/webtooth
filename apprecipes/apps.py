from django.apps import AppConfig


class ApprecipesConfig(AppConfig):
    name = 'apprecipes'
    verbose_name = 'Gestión de Recetas'

    def ready(self):
        from webtooth import signals