from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry

# Register your models here.
from apppatients.models import Patient
from apppatients.models import Adress
from apppatients.models import Navigation
from apppatients.models import File
from apppatients.models import Propertie
from apppatients.models import Import
from apppatients.models import Task
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

class NavigationAdmin(admin.ModelAdmin):
	list_display = ('eventTime', 'userName','permission', 'method', 'path', 'host', 'varSession')
	list_filter = ['eventTime', 'userCode']
	date_hierarchy = ('eventTime')
	ordering = ('-eventTime',)

	class Media:
		css = {
			'all':('css/customAdmin.css',)
		}

	def has_add_permission(self, request):
		return False
	def has_change_permission(self, request, obj=None):
		return False
	def has_delete_permission(self, request, obj=None):
		return False


class FileAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'fechaSubida', 'path')
	list_filter = ['fechaSubida']
	date_hierarchy = ('fechaSubida')
	ordering = ('-fechaSubida',)

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


class ImportAdmin(admin.ModelAdmin):
	list_display = ('tipoSubida', 'fechaSubida', 'path', 'importado')
	list_filter = ['fechaSubida', 'importado']
	date_hierarchy = ('fechaSubida')
	ordering = ('-fechaSubida',)

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


class TaskAdmin(admin.ModelAdmin):
	list_display = ('userCode', 'userName', 'nameTask', 'descTask',
	                'dateCreate', 'dateExecute', 'status')
	list_filter = ['dateCreate', 'dateExecute', 'userCode', 'status']
	date_hierarchy = ('dateCreate')
	ordering = ('-dateCreate',)

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

admin.site.register(Patient,PatientAdmin)
admin.site.register(Adress,AdressAdmin)
admin.site.register(Permission)
admin.site.register(LogEntry,LogAdmin)
admin.site.register(Navigation,NavigationAdmin)
admin.site.register(File,FileAdmin)
admin.site.register(Propertie,PropertieAdmin)
admin.site.register(Import,ImportAdmin)
admin.site.register(Task,TaskAdmin)
admin.site.register(Recipe,RecipeAdmin)
