from django.db import models
from webtooth.mixins import AuditModel

# Create your models here.
class Patient(AuditModel, models.Model):
	userId = models.IntegerField(blank=True, null=True)
	userName = models.CharField(blank=True, null=True, max_length=100)
	nombre=models.CharField(max_length=50, verbose_name="Nombre")
	apellidoPaterno=models.CharField(max_length=50, verbose_name="Apellido paterno")
	apellidoMaterno = models.CharField(blank=True, null=True, max_length=50, verbose_name="Apellido materno")
	rfc=models.CharField(blank=True,null=True,max_length=13, verbose_name="RFC")
	email=models.EmailField(blank=True,null=True,verbose_name="Correo electrónico")
	telefono = models.CharField(blank=True, null=True, max_length=10, verbose_name="Teléfono")
	numexp=models.CharField(max_length=15,verbose_name="Número de expediente")
	fechaAlta = models.DateTimeField(blank=True, null=True, verbose_name="Fecha alta")
	activo=models.BooleanField(blank=True,null=True,verbose_name="Activo")
	eliminado=models.BooleanField(blank=True,null=True,verbose_name="Eliminado")
	sexo = models.CharField(blank=True, null=True,max_length=50, verbose_name="Sexo")
	ocupacion = models.CharField(blank=True, null=True, max_length=75, verbose_name="Ocupación")
	fechaNacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha nacimiento")

	fechaUpdate = models.DateTimeField(blank=True, null=True, verbose_name="Fecha actualización")
	foto = models.ImageField(blank=True, null=True, verbose_name="Foto", upload_to="img")

	def __str__(self):
		return "{}".format(self.numexp)

	class Meta:
		verbose_name = 'paciente'
		verbose_name_plural = 'Pacientes'
		permissions = [("addPatient","Agregar paciente"),("viewPatient","Ver paciente"),("deletePatient","Eliminar paciente"),("updatePatient","Actualizar paciente")]

class Adress(AuditModel, models.Model):
	userId = models.IntegerField(blank=True, null=True)
	userName = models.CharField(blank=True, null=True, max_length=100)
	calle=models.CharField(max_length=50, verbose_name="Calle")
	numeroExt=models.CharField(max_length=50, verbose_name="Número exterior")
	numeroInt=models.CharField(max_length=50, verbose_name="Número interior")
	ciudad=models.CharField(max_length=50, verbose_name="Ciudad")
	estado=models.CharField(max_length=50,verbose_name="Estado")
	cp=models.CharField(max_length=6,verbose_name="Código Postal")	

	patient = models.OneToOneField(Patient, on_delete = models.CASCADE, verbose_name="Paciente")

	def __str__(self):
		return "dirección: {}, {} {}".format(self.calle,self.ciudad,self.estado)

	class Meta:
		verbose_name = 'dirección'
		verbose_name_plural = 'Direcciones'
		permissions = [("viewAdress", "Ver dirección")]
