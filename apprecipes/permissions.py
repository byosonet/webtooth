APP_NAME_MANAGEMENT_RECIPES = 'apprecipes.'

#Redirect a pagina no tiene permisos
def notPermission():
	return '/permission/required/'

#Gestion de permisos para Recetas
def listRecipe():
	return APP_NAME_MANAGEMENT_RECIPES+'listRecipe'
def addRecipe():
	return APP_NAME_MANAGEMENT_RECIPES+'addRecipe'
def deleteRecipe():
	return APP_NAME_MANAGEMENT_RECIPES+'deleteRecipe'
