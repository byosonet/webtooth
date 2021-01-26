from django.db import models

# Create your models here.
class Product(models.Model):
	nombre=models.CharField(max_length=50, verbose_name="Nombre")
	marca=models.CharField(max_length=50, verbose_name="Marca")
	cantidad=models.IntegerField(verbose_name="Existencias")
	fechaAlta=models.DateField(max_length=50, verbose_name="Fecha alta")
	fechaBaja=models.DateField(blank=True,null=True,verbose_name="Fecha baja")	

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name = 'producto'
		verbose_name_plural = 'Productos'
