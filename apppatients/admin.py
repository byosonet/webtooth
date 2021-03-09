from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry

# Register your models here.
from apppatients.models import Patient
from apppatients.models import Adress
from apppatients.models import Propertie
from apppatients.models import Recipe

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
	
class LogAdmin(admin.ModelAdmin):
	list_display = ('action_time','_user','_content_type','_change_message','_object_repr')
	list_filter = ['action_time','user']
	date_hierarchy = ('action_time')
	ordering = ('-action_time',)

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

	def _user(self, obj):
		return obj.user.first_name + obj.user.last_name
	_user.short_description = 'Usuario'

	def _content_type(self, obj):
		if obj.content_type.model == 'logentry':
			obj.content_type.model = "logs"
			return obj.content_type
		return obj.content_type
	_content_type.short_description = 'Modelo afectado'

	def _change_message(self, obj):
		return obj.change_message
	_change_message.short_description = 'Tipo de acción'

	def _object_repr(self, obj):
		return obj.object_repr
	_object_repr.short_description = 'Bitácora de registro'


class PropertieAdmin(admin.ModelAdmin):
	list_display = ('userId', 'key', 'value')
	list_filter = ['userId']
	ordering = ('-userId',)

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


class RecipeAdmin(admin.ModelAdmin):
	list_display = ('userCode', 'userName', 'nameRecipe', 'subjectRecipe',
	                'emailRecipe', 'descRecipe', 'dateSend', 'stateRecipe')
	list_filter = ['dateSend', 'userCode', 'stateRecipe']
	date_hierarchy = ('dateSend')
	ordering = ('-dateSend',)

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
admin.site.register(Permission)
admin.site.register(LogEntry,LogAdmin)
admin.site.register(Propertie,PropertieAdmin)
admin.site.register(Recipe,RecipeAdmin)
