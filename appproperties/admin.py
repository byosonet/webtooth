from django.contrib import admin

# Register your models here.
from appproperties.models import Propertie

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

def validUser(request):
	usercode = request.user.get_username()	
	if usercode == 'admin':
		return True
	else:
		return False

admin.site.register(Propertie,PropertieAdmin)
