from django.db import models
from . mixins import AuditModel

# Create your models here.
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
