from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry

# Register your models here.
from appfiles.models import File

class FileAdmin(admin.ModelAdmin):
	list_display = ('userName','nombre', 'fechaSubida', 'path')
	list_filter = ['fechaSubida','userName']
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
	def has_module_permission(self, request):
		return validUser(request)

def validUser(request):
	usercode = request.user.get_username()	
	if usercode == 'admin':
		return True
	else:
		return False

admin.site.register(File,FileAdmin)
