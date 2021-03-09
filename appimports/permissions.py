APP_NAME_MANAGEMENT_IMPORTS = 'appimports.'

#Redirect a pagina no tiene permisos
def notPermission():
	return '/permission/required/'

#Gestion de permisos para Importar
def importFile():
	return APP_NAME_MANAGEMENT_IMPORTS+'importFile'
