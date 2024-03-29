from django.contrib import admin

# Register your models here.
from apptasks.models import Task

class TaskAdmin(admin.ModelAdmin):
	list_display = ('userName', 'nameTask', 'descTask',
	                'dateCreate', 'dateExecute', 'status')
	list_filter = ['dateCreate', 'dateExecute', 'userName', 'status']
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
	def has_module_permission(self, request):
		return validUser(request)

def validUser(request):
	usercode = request.user.get_username()	
	if usercode == 'admin':
		return True
	else:
		return False

admin.site.register(Task,TaskAdmin)
