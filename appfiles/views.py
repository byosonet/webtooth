from django.contrib.auth.decorators import login_required, permission_required
from webtooth.decorators import validRequest
from django.shortcuts import render

from . models import File
from . forms import FileForm
from . config import validErrors

import os
from django.conf import settings
from appfiles.permissions import *
from webtooth.config import logger, getLogin, currentLocalTime, filterQuery
from django.contrib import messages
from webtooth.signals import getUser

# Create your views here.
log = logger('appfiles', True)

@login_required(login_url=getLogin())
@permission_required(addFile(), login_url=notPermission())
@validRequest
def altaArchivo(request):
    log.info("[Load view method: altaArchivo]")    
    user = getUser()
    if request.method == 'POST':
        formFile = FileForm(request.POST, request.FILES)
        if formFile.is_valid():
            file = formFile.save(commit=False)
            file.fechaSubida = currentLocalTime()
            fileName = file.nombre+"."+file.path.name[::-1].split(".")[0][::-1]            
            file.path.name = fileName
            file.userId = userRequest()
            file.userName = user.get_full_name()
            log.info("Formulario valido, preparando alta de archivo...")
            dataFile = formFile.cleaned_data
            printLogFiles("Data recibida del formulario archivo: "+str(dataFile))
            file.save()            
            log.info("Se ha agregado a la BD el nuevo registro de archivo")
            messages.success(request, f"El archivo {fileName} ha sido agregado correctamente")
            formFile = FileForm()
            return render(request, "file/altaArchivo.html", {"form": formFile})
        else:
            log.error("Formulario recibido no pasa la validacion...")
            validErrors(formFile)
    else:
        formFile = FileForm()
    return render(request, "file/altaArchivo.html", {"form": formFile})


@login_required(login_url=getLogin())
@permission_required(listFile(), login_url=notPermission())
@validRequest
def listarArchivo(request):
    log.info("[Load view method: listarArchivo]")
    log.info("Obteniendo lista de archivos")    
    listadoArchivos = File.objects.filter(filterQuery()).order_by('-fechaSubida')    
    return render(request, "file/listaArchivos.html", {"listaArchivo": listadoArchivos})


@login_required(login_url=getLogin())
@permission_required(deleteFile(), login_url=notPermission())
@validRequest
def eliminarArchivo(request, idFile):
    log.info("[Load view method: eliminarArchivo(idFile)]")
    log.info("idFile: "+str(idFile))    
    listadoArchivos = File.objects.filter(filterQuery()).order_by('-fechaSubida')
    try:
        log.info("ID File recibido: "+str(idFile))
        user = getUser()
        if user.get_username() == 'admin':
            file = File.objects.get(pk=idFile)
        else:
            file = File.objects.get(pk=idFile, userId=userRequest())
        fileOld = file.path
        log.info("Se ha eliminado el archivo de BD: {}".format(file.fileName))
        fileN = file.nombre+"."+file.path.name[::-1].split(".")[0][::-1] 
        file.delete()
        try:
            if fileOld:
                os.remove(settings.MEDIA_PATH+str(fileOld))
                log.info("Se ha eliminado el archivo: "+str(fileOld))
        except Exception as ex:
            log.error("No se pudo eliminar el archivo {} por el siguiente error:  {}".format(
                fileOld, ex))
        messages.success(request, "El archivo: {} fue eliminado correctamente".format(str(fileN)))
        return render(request, "file/listaArchivos.html", {"listaArchivo": listadoArchivos})
    except Exception as ex:
        log.error("Error: "+str(ex))
        listadoArchivos = None
        return render(request, "file/listaArchivos.html", {"listaArchivo": listadoArchivos})

def userRequest():
    user = getUser()
    return user.id

def printLogFiles(register):
    log.debug(register)