from django.db import models
from webtooth.mixins import AuditModel

# Create your models here.
class Propertie(AuditModel, models.Model):
	userId = models.IntegerField(blank=True, null=True)
	key = models.CharField(max_length=100, verbose_name="key")
	value = models.CharField(blank=True, null=True, max_length=100, verbose_name="value")

	def __str__(self):
		return "key: {}, value: {}".format(self.key, self.value)

	class Meta:
		verbose_name = 'propiedad'
		verbose_name_plural = 'Propiedades'
