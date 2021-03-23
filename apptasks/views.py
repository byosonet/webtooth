from django.contrib.auth.decorators import login_required, permission_required
from webtooth.decorators import validRequest
from django.shortcuts import render, redirect

from . models import Task
from . forms import TaskForm
from . config import validErrors
from . query import filterByIdTask

from apptasks.permissions import *
from webtooth.config import logger, getLogin, currentLocalTime, getListTask
from django.contrib import messages
from webtooth.signals import getUser

# Create your views here.
log = logger('apptasks', True)

@login_required(login_url=getLogin())
@permission_required(addTask(), login_url=notPermission())
@validRequest
def altaTarea(request):
    log.info("[Load view method: altaTarea]")
    user = getUser()
    log.info("Obteniendo lista de tareas")

    if user.get_username() == 'admin':
        listadoTareas = Task.objects.filter().order_by('-id')
    else:
        listadoTareas = Task.objects.filter(userCode=user.get_username()).order_by('-id')

    if request.method == 'POST':
        taskForm = TaskForm(request.POST)
        if all([taskForm.is_valid()]):
            task = taskForm.save(commit=False)
            task.nameTask = task.nameTask.title()
            task.descTask = task.descTask.title()

            task.userId = user.id
            task.userCode = user.get_username()
            task.userName = user.get_full_name()

            dataTask = taskForm.cleaned_data
            printLogTasks("Data recibida del formulario Task: "+str(dataTask))
            task.save()

            log.info("Se ha agregado a la BD el nuevo registro")

            messages.success(request, f"¡La tarea {task.nameTask} ha sido agregada correctamente!")
            ###return buscarTaskId(request, task.id)
            return redirect("buscarTaskId",idTask=task.id)

        else:
            log.error("Formulario recibido no pasa la validacion...")
            messages.error(request, "¡Algunos campos necesitan llenarse de forma correcta!")
            validErrors(taskForm)
    else:
        taskForm = TaskForm()
    return render(request, "task/altaTarea.html", {"form": taskForm, "listadoTareas": listadoTareas})


@login_required(login_url=getLogin())
@validRequest
def buscarTaskId(request, idTask):
    log.info("[Load view method: buscarTaskId(idTask)]")
    log.info("idTask: "+str(idTask))
    taskForm = TaskForm()
    try:
        user = getUser()
        getListTask(request, user.get_username())
        result = filterByIdTask(idTask, taskForm)        
        return render(request, "task/detailTask.html", {"form": result, "idTask": idTask})

    except Exception as ex:
        log.error("Error al buscar por id: "+str(ex))
        return render(request, "task/detailTask.html", {"form": None})

@login_required(login_url=getLogin())
@validRequest
def actualizarTask(request, idTask):
    log.info("[Load view method: actualizarTask(idTask)]")
    log.info("idTask: "+str(idTask))
    formTask = None    
    try:
        user = getUser()
        if user.get_username() == 'admin':
            obj = Task.objects.get(pk=idTask)
        else:
            obj = Task.objects.get(pk=idTask, userId=userRequest())
        formTask = TaskForm(request.POST, instance=obj)
        if all([formTask.is_valid()]):
            log.info("Formulario valido, actualizando datos de Tarea...")     

            if obj.status:
                obj.dateExecute = currentLocalTime()

            dataTask = formTask.cleaned_data
            printLogTasks("Data task recibida: "+str(dataTask))
            formTask.save()            

            log.info("Se ha actualizado el registro en BD para la tarea {}".format(dataTask['nameTask']))
            messages.success(request, "¡Los datos han sido actualizados correctamente!")
            ###return buscarTaskId(request, idTask)
            return redirect("buscarTaskId",idTask=idTask)
        else:
            log.error("Formulario recibido no pasa la validacion...")
            validErrors(formTask)
            ###return buscarTaskId(request, idTask)
            return redirect("buscarTaskId",idTask=idTask)
    except Exception as ex:
        log.error("Error: "+str(ex))
        return render(request, "task/detailTask.html", {"form": formTask, "idTask": idTask})

def printLogTasks(register):
    log.debug(register)

def userRequest():
    user = getUser()
    return user.id