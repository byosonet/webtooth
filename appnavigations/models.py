from django.db import models

# Create your models here.

class Navigation(models.Model):
	userName = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nombre")
	userId = models.IntegerField(blank=True, null=True)
	userCode = models.CharField(blank=True, null=True, max_length=100, verbose_name="Usuario")
	permission = models.CharField(blank=True, null=True, max_length=3999, verbose_name="Permisos")
	method = models.CharField(blank=True, null=True, max_length=10, verbose_name="Tipo de petición")
	path = models.CharField(blank=True, null=True, max_length=200, verbose_name="Url del servicio")
	status = models.IntegerField(blank=True, null=True, verbose_name="Estado de la respuesta")
	data = models.TextField(blank=True, null=True, verbose_name="Datos enviados")
	host = models.CharField(blank=True, null=True, max_length=100, verbose_name="IP de origen")
	file = models.CharField(blank=True, null=True, max_length=500, verbose_name="Archivo procesado")
	varSession = models.TextField(blank=True, null=True, verbose_name="Variables de sesión")
	eventTime = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Hora de la acción")

	def __str__(self):
		return "Navigation Host: {}, Time: {}".format(self.host,self.eventTime)

	class Meta():
		verbose_name = 'navegación'
		verbose_name_plural = 'Navegaciones'
		permissions = [("viewListNavigation", "Ver historial de navegación")]