from django.contrib import admin

# Register your models here.
from django.contrib.admin.models import LogEntry
from django.contrib.sites.models import Site

admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
	fields = ('id', 'domain', 'name')
	list_display = ('id', 'domain', 'name')
	list_display_links = ('domain',)
	list_filter = ['domain']

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


def validUser(request):
	usercode = request.user.get_username()	
	if usercode == 'admin':
		return True
	else:
		return False

admin.site.register(LogEntry,LogAdmin)
admin.site.register(Site, SiteAdmin)
