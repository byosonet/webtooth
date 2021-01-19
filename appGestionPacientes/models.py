from django.db import models
from appGestionPacientes.mixins import AuditModel

# Create your models here.
class Patient(AuditModel, models.Model):
	nombre=models.CharField(max_length=50, verbose_name="Nombre")
	apellidoPaterno=models.CharField(max_length=50, verbose_name="Apellido paterno")
	apellidoMaterno = models.CharField(blank=True, null=True, max_length=50, verbose_name="Apellido materno")
	rfc=models.CharField(blank=True,null=True,max_length=13, verbose_name="RFC")
	email=models.EmailField(blank=True,null=True,verbose_name="Correo electrónico")
	telefono = models.CharField(blank=True, null=True, max_length=10, verbose_name="Teléfono")
	numexp=models.CharField(max_length=15,verbose_name="Número de expediente")
	fechaAlta = models.DateTimeField(auto_now_add=True, blank=True, null=True,verbose_name="Fecha alta")
	activo=models.BooleanField(blank=True,null=True,verbose_name="Activo")
	eliminado=models.BooleanField(blank=True,null=True,verbose_name="Eliminado")

	fechaUpdate = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Fecha actualización")
	foto = models.ImageField(blank=True, null=True, verbose_name="Foto", upload_to="img")

	def __str__(self):
		return "expediente: {}, de {} {}".format(self.numexp,self.nombre,self.apellidoPaterno)

	#Nombre de la tabal en la BD
	class Meta:
		verbose_name = 'paciente'
		verbose_name_plural = 'Pacientes'
		permissions = [("addPatient","Agregar paciente"),("viewPatient","Ver paciente"),("deletePatient","Eliminar paciente"),("updatePatient","Actualizar paciente")]

class Adress(AuditModel, models.Model):
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


class File(AuditModel, models.Model):
	nombre = models.CharField(max_length=50, verbose_name="Nombre del archivo")
	fechaSubida = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Fecha de subida")
	path = models.FileField(blank=True, null=True,verbose_name="Archivo", upload_to="upload")

	def __str__(self):
		return "achivo: {}".format(self.path.name.split("/")[1])

	def fileName(self):
		return self.path.name.split("/")[1]

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

class Propertie(models.Model):
	userId = models.IntegerField(blank=True, null=True)
	key = models.CharField(max_length=100, verbose_name="key")
	value = models.CharField(blank=True, null=True, max_length=100, verbose_name="value")

	def __str__(self):
		return "key: {}, value: {}".format(self.key, self.value)

	class Meta:
		verbose_name = 'propiedad'
		verbose_name_plural = 'Propiedades'


class Import(AuditModel, models.Model):
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
