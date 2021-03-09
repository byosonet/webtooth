from django.db import models
from . mixins import AuditModel

# Create your models here.

class Import(AuditModel, models.Model):
	userId = models.IntegerField(blank=True, null=True)
	userName = models.CharField(blank=True, null=True, max_length=100)
	tipoSubida = models.CharField(max_length=50, verbose_name="Tipo de fichero")
	fechaSubida = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Fecha de subida")
	path = models.FileField(blank=True, null=True,verbose_name="Archivo", upload_to="upload-xls")
	importado = models.BooleanField(blank=True, null=True, verbose_name="Importado")

	def __str__(self):
		return "achivo: {}".format(self.path.name.split("/")[1])

	def fileName(self):
		return self.path.name.split("/")[1]

	class Meta:
		verbose_name = 'importado'
		verbose_name_plural = 'Importados'
		permissions = [("importFile","Subir archivo")]
