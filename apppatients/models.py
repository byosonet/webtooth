from django.db import models
from apppatients.mixins import AuditModel

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
		return "expediente: {}, de {} {}".format(self.numexp,self.nombre,self.apellidoPaterno)

	#Nombre de la tabal en la BD
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

class Propertie(models.Model):
	userId = models.IntegerField(blank=True, null=True)
	key = models.CharField(max_length=100, verbose_name="key")
	value = models.CharField(blank=True, null=True, max_length=100, verbose_name="value")

	def __str__(self):
		return "key: {}, value: {}".format(self.key, self.value)

	class Meta:
		verbose_name = 'propiedad'
		verbose_name_plural = 'Propiedades'


class Task(AuditModel, models.Model):
	userId = models.IntegerField(blank=True, null=True)
	userCode = models.CharField(blank=True, null=True, max_length=100, verbose_name="Usuario")
	userName = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nombre")
	
	nameTask = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nombre de la tarea")
	descTask = models.CharField(blank=True, null=True, max_length=3999, verbose_name="Descripción de la tarea")

	dateCreate = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de creación")
	dateExecute = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de ejecución")

	status = models.BooleanField(blank=True, null=True, verbose_name="Estado de la tarea")

	def __str__(self):
		return "Task: userID: {}, userCode: {}, username: {}, nameTask: {}, descTask: {}".format(self.userId, self.userCode, self.userName, self.nameTask, self.descTask)

	class Meta():
		verbose_name = 'Tarea'
		verbose_name_plural = 'Tareas'
		permissions = [("listTask", "Listar tareas"), ("addTask","Agregar tarea"), ("deleteTask", "Eliminar tarea")]


class Recipe(AuditModel, models.Model):
	userId = models.IntegerField(blank=True, null=True)
	userCode = models.CharField(blank=True, null=True, max_length=100, verbose_name="Usuario")
	userName = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nombre de usuario")

	nameRecipe = models.CharField(blank=True, null=True, max_length=100, verbose_name="Nombre del paciente")
	subjectRecipe = models.CharField(blank=True, null=True, max_length=100, verbose_name="Asunto")
	emailRecipe = models.CharField(blank=True, null=True, max_length=100, verbose_name="Email")
	descRecipe = models.CharField(blank=True, null=True, max_length=3999, verbose_name="Receta")
	stateRecipe = models.CharField(blank=True, null=True, max_length=100, verbose_name="Estado")
	
	dateSend = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Fecha de envío")

	def __str__(self):
		return "Recipe: nameRecipe: {}, subjectRecipe: {}, emailRecipe: {}".format(self.nameRecipe, self.subjectRecipe, self.emailRecipe)

	class Meta():
		verbose_name = 'Receta'
		verbose_name_plural = 'Recetas'
		permissions = [("listRecipe", "Listar recetas"), ("addRecipe","Agregar receta"), ("deleteRecipe", "Eliminar receta")]
