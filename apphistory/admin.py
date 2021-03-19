from django.contrib import admin

# Register your models here.
from apphistory.models import Group, Study, History


class GroupAdmin(admin.ModelAdmin):
	list_display = ('nombre','user','fechaAlta','fechaUpdate')
	list_filter = ['fechaAlta','user']
	date_hierarchy = ('fechaAlta')
	ordering = ('-fechaAlta',)

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

class StudyAdmin(admin.ModelAdmin):
	list_display = ('nombre','grupo','user','fechaAlta','fechaUpdate')
	list_filter = ['fechaAlta','user']
	date_hierarchy = ('fechaAlta')
	ordering = ('-fechaAlta',)

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

class HistoryAdmin(admin.ModelAdmin):
	list_display = ('patient','grupo','estudio','check','fechaAlta','fechaUpdate','user')
	list_filter = ['fechaAlta','user']
	date_hierarchy = ('fechaAlta')
	ordering = ('-fechaAlta',)

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

admin.site.register(Group,GroupAdmin)
admin.site.register(Study,StudyAdmin)
admin.site.register(History,HistoryAdmin)