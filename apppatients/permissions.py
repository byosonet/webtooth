APP_NAME_MANAGEMENT_PATIENT = 'apppatients.'

#Redirect a pagina no tiene permisos
def notPermission():
	return '/permission/required/'

#Gestion de permisos para Pacientes
def addPatient():
	return APP_NAME_MANAGEMENT_PATIENT+'addPatient'
def viewPatient():
	return APP_NAME_MANAGEMENT_PATIENT+'viewPatient'
def updatePatient():
	return APP_NAME_MANAGEMENT_PATIENT+'updatePatient'
def deletePatient():
	return APP_NAME_MANAGEMENT_PATIENT+'deletePatient'

#Gestion de permisos para Direcciones
def viewAdress():
	return APP_NAME_MANAGEMENT_PATIENT+'viewAdress'

#Gestion de permisos para Recetas
def listRecipe():
	return APP_NAME_MANAGEMENT_PATIENT+'listRecipe'
def addRecipe():
	return APP_NAME_MANAGEMENT_PATIENT+'addRecipe'
def deleteRecipe():
	return APP_NAME_MANAGEMENT_PATIENT+'deleteRecipe'
