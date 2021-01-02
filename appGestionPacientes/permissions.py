APP_NAME_MANAGEMENT_PATIENT = 'appGestionPacientes.'

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

#Gestion de permisos para Archivos
def listFile():
	return APP_NAME_MANAGEMENT_PATIENT+'listFile'
def addFile():
	return APP_NAME_MANAGEMENT_PATIENT+'addFile'
def deleteFile():
	return APP_NAME_MANAGEMENT_PATIENT+'deleteFile'

def listNavigation():
	return APP_NAME_MANAGEMENT_PATIENT+'viewListNavigation'

#Gestion de permisos para Importar
def importFile():
	return APP_NAME_MANAGEMENT_PATIENT+'importFile'