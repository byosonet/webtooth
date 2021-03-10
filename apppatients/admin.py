from django.contrib import admin

# Register your models here.
from apppatients.models import Patient
from apppatients.models import Adress

class PatientAdmin(admin.ModelAdmin):
	readonly_fields = ("fechaAlta", "fechaUpdate","numexp","foto")
	list_display = ("numexp", "fechaAlta", "nombre", "apellidoPaterno","apellidoMaterno", "email", "telefono", "fechaUpdate")
	search_fields = ("numexp", "nombre", "apellidoPaterno","email")
	list_filter = ("fechaAlta", "fechaUpdate")
	date_hierarchy = ("fechaAlta")
	ordering = ('-fechaUpdate',)

	class Media:
		css = {
			'all': ('css/customAdmin.css',)
		}

	def has_add_permission(self, request):
		return False
	def has_change_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	def has_module_permission(self, request):
		return validUser(request)

class AdressAdmin(admin.ModelAdmin):
	list_display = ("ciudad", "estado","numeroExt", "numeroInt", "calle", "cp","patient")
	search_fields = ("cp", "ciudad", "estado","calle")
	readonly_fields = ["patient"]

	class Media:
		css = {
			'all': ('css/customAdmin.css',)
		}

	def has_add_permission(self, request):
		return False
	def has_change_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False
	def has_module_permission(self, request):
		return validUser(request)
	
def validUser(request):
	usercode = request.user.get_username()	
	if usercode == 'admin':
		return True
	else:
		return False

admin.site.register(Patient,PatientAdmin)
admin.site.register(Adress,AdressAdmin)
