from django.db import models
from . mixins import AuditModel

# Create your models here.

def user_directory_path(instance, filename):	
	return 'upload/{0}/{1}'.format(instance.userId, filename)

class File(AuditModel, models.Model):
	userId = models.IntegerField(blank=True, null=True)
	userName = models.CharField(blank=True, null=True, max_length=100)
	nombre = models.CharField(max_length=50, verbose_name="Nombre del archivo")
	fechaSubida = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Fecha de subida")
	path = models.FileField(blank=True, null=True,verbose_name="Archivo", upload_to=user_directory_path)

	def __str__(self):
		return "achivo: {}".format(self.path.name.split("/")[1])

	def fileName(self):
		return self.path.name.split("/")[2]

	def typeFile(self):
		ext = self.path.name.split(".")[1]
		if ext == 'pdf':
			return 'file-pdf'
		elif ext == 'txt':
			return 'file-signature'
		elif ext == 'xlsx' or ext == 'xls':
			return 'file-excel'
		elif ext == 'zip' or ext == 'rar':
			return 'file-archive'
		elif ext == 'docx' or ext == 'doc':
			return 'file-word'
		elif ext == 'png' or ext == 'jpg' or ext == 'jpeg':
			return 'file-image'
		elif ext == 'ppt' or ext == 'pptx':
			return 'file-powerpoint'
		elif ext == 'csv':
			return 'file-csv'
		elif ext == 'html':
			return 'file-contract'
		elif ext == 'css':
			return 'file-code'
		else:
			return 'file'

	class Meta:
		verbose_name = 'archivo'
		verbose_name_plural = 'Archivos'
		permissions = [("listFile", "Listar archivos"), ("addFile","Agregar archivo"), ("deleteFile", "Eliminar archivo")]
