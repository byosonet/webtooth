APP_NAME_MANAGEMENT_HISTORY = 'apphistory.'

#Redirect a pagina no tiene permisos
def notPermission():
	return '/permission/required/'

#Gestion de permisos para Grupos
def viewGroup():
	return APP_NAME_MANAGEMENT_HISTORY+'viewGroup'
def addGroup():
	return APP_NAME_MANAGEMENT_HISTORY+'addGroup'
def deleteGroup():
	return APP_NAME_MANAGEMENT_HISTORY+'deleteGroup'
def updateGroup():
	return APP_NAME_MANAGEMENT_HISTORY+'updateGroup'