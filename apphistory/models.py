from django.db import models
from webtooth.mixins import AuditModel
from django.contrib.auth.models import User
from apppatients.models import Patient

# Create your models here.
class Group(AuditModel, models.Model):
    nombre=models.CharField(max_length=50, verbose_name="Grupo de estudio")
    fechaAlta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha alta")
    fechaUpdate = models.DateTimeField(auto_now_add=True, verbose_name="Fecha actualización")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Usuario")

    def __str__(self):
        return "Grupo: {}".format(self.nombre)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        permissions = [("addGroup","Agregar grupo"),("viewGroup","Ver grupo"),
        ("deleteGroup","Eliminar grupo"),("updateGroup","Actualizar grupo")]


class Study(AuditModel, models.Model):
    nombre=models.CharField(max_length=50, verbose_name="Estudio")
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Grupo de Estudio")
    fechaAlta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha alta")
    fechaUpdate = models.DateTimeField(auto_now_add=True, verbose_name="Fecha actualización")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Usuario")

    def __str__(self):
        return "Study: {}".format(self.nombre)

    class Meta:
        verbose_name = 'Estudio'
        verbose_name_plural = 'Estudios'
        permissions = [("addStudy","Agregar estudio"),("viewStudy","Ver estudio"),
        ("deleteStudy","Eliminar estudio"),("updateStudy","Actualizar estudio")]

class History(AuditModel, models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Paciente")
    grupo = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Grupo de estudio")
    estudio = models.ForeignKey(Study, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Estudio")
    check = models.BooleanField(blank=True,null=True,verbose_name="Check")
    fechaAlta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha alta")
    fechaUpdate = models.DateTimeField(auto_now_add=True, verbose_name="Fecha actualización")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Usuario")

    def __str__(self):
        return "History of patient: {}, {}, {}, check: {}".format(self.patient,self.grupo, self.estudio,self.check)

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = 'Historial'
        permissions = [("addHistory","Agregar historia"),("viewHistory","Ver historia"),
        ("deleteHistory","Eliminar historia"),("updateHistory","Actualizar historia")]
