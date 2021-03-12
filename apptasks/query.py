from . models import Task
from webtooth.config import logger
from webtooth.signals import getUser

log = logger('apptasks.query', False)

def filterByIdTask(idTask, formTask):
	printLogQuery("Id recibido for task: "+str(idTask))	
	user = getUser()
	if user.get_username() == 'admin':
		task = Task.objects.get(pk=idTask)
	else:
		task = Task.objects.get(pk=idTask, userId=userRequest())

	if task:
		log.info("Task encontrado: {}".format(task.nameTask))
		formTask.fields['nameTask'].initial = task.nameTask
		formTask.fields['descTask'].initial = task.descTask
		formTask.fields['status'].initial = task.status
		formTask.fields['dateCreate'].initial = task.dateCreate
		formTask.fields['dateExecute'].initial = task.dateExecute
		return formTask
	else:
		return None

def printLogQuery(register):
	log.debug(register)

def userRequest():
    user = getUser()
    return user.id