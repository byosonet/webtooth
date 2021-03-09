APP_NAME_MANAGEMENT_FILES = 'appfiles.'

#Redirect a pagina no tiene permisos
def notPermission():
	return '/permission/required/'

#Gestion de permisos para Archivos
def listFile():
	return APP_NAME_MANAGEMENT_FILES+'listFile'
def addFile():
	return APP_NAME_MANAGEMENT_FILES+'addFile'
def deleteFile():
	return APP_NAME_MANAGEMENT_FILES+'deleteFile'