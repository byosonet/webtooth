APP_NAME_MANAGEMENT_NAVIGATIONS = 'appnavigations.'

#Redirect a pagina no tiene permisos
def notPermission():
	return '/permission/required/'

#Gestion de permisos para historial de navegación
def listNavigation():
	return APP_NAME_MANAGEMENT_NAVIGATIONS+'viewListNavigation'