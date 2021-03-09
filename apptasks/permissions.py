APP_NAME_MANAGEMENT_TASKS = 'apptasks.'

#Redirect a pagina no tiene permisos
def notPermission():
	return '/permission/required/'

#Gestion de permisos para Tareas
def listTask():
	return APP_NAME_MANAGEMENT_TASKS+'listTask'
def addTask():
	return APP_NAME_MANAGEMENT_TASKS+'addTask'
def deleteTask():
	return APP_NAME_MANAGEMENT_TASKS+'deleteTask'
