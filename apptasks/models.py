from django.db import models
from webtooth.mixins import AuditModel

# Create your models here.

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
