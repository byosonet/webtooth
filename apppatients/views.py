from apppatients import urls
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from webtooth.config import currentLocalTime,filterQuery, updatePropertie, loadPropertie
from django.http import HttpResponse
import json

import os
from django.conf import settings

from apppatients.models import Patient, Adress, File, Navigation, Import, Task, Recipe, Propertie
from apppatients.forms import ContactForm, PatientForm, AdressForm, FileForm, ImportForm, TaskForm
from apppatients.config import validErrors
from apppatients.query import filterSearch, filterByIdPatient, generateKlave, filterByIdPatientAdress, filterPatientDelete, filterByIdTask

from webtooth.config import logger, sendEmailContact, getLogin, getListTask
from apppatients.permissions import *
from webtooth.decorators import validRequest
from django.contrib import messages
from apppatients.signals import getUser

import pandas as pd

log = logger('apppatients', True)

@login_required(login_url=getLogin())
@permission_required(viewPatient(),login_url=notPermission())
@validRequest
def buscarPaciente(request):
    log.info("[Load view method: buscarPaciente]")
    log.info("Buscando paciente")
    return render(request,"patient/buscarPaciente.html")

@login_required(login_url=getLogin())
@permission_required(viewPatient(),login_url=notPermission())
@validRequest
def buscarNombre(request):
    log.info("[Load view method: buscarNombre]")
    try:
        listadoPacientes = filterSearch(request)
        return render(request, "patient/listaPacientes.html", {"listaPaciente":listadoPacientes,"txtbuscado":"No se encontraron datos"})
    except Exception as ex:
        log.error("Faltan campos por llenarse: "+str(ex))
        message="Para poder realizar la acción, primero se debe introducir los parámetros faltantes."
        data = {"data":message}
        return render(request,'error/error.html', data)

@login_required(login_url=getLogin())
@permission_required(viewPatient(),login_url=notPermission())
@validRequest
def listarPaciente(request):
    log.info("[Load view method: listarPaciente]")
    log.info("Obteniendo lista de pacientes")    
    listadoPacientes = Patient.objects.filter(filterQuery()).order_by('-fechaUpdate')[:settings.MAX_ROWS_QUERY_MODEL]
    return render(request, "patient/listaPacientes.html", {"listaPaciente":listadoPacientes})

@login_required(login_url=getLogin())
@permission_required(viewPatient(),login_url=notPermission())
@validRequest
def contactoPaciente(request):
    log.info("[Load view method: contactoPaciente]")    
    listadoEnviados = Recipe.objects.filter(filterQuery()).order_by('-dateSend')[:settings.MAX_ROWS_QUERY_MODEL]
    if request.method=='POST':
        formContact = ContactForm(request.POST)
        if formContact.is_valid():
            log.info("Formulario valido, preparando envío...")

            recipe = formContact.save(commit=False)
            recipe.nameRecipe = recipe.nameRecipe.title()
            recipe.subjectRecipe = recipe.subjectRecipe
            user = getUser()
            recipe.userId = user.id
            recipe.userCode = user.get_username()
            recipe.userName = user.get_full_name()
            
            dataContact = formContact.cleaned_data
            printLogPatients("Data recibida del formulario Recipe: "+str(dataContact))
            log.info("Se ha agregado a la BD el nuevo registro")
            
            email=sendEmailContact(dataContact)
            if email == None:
                recipe.stateRecipe = 'No enviado'
                messages.error(
                    request, f"Servidor de correo no disponible, intentelo más tarde.")
            else:
                recipe.stateRecipe = 'Enviado'
                messages.success(request, f"El correo se ha enviado correctamente ha: {email}")
            recipe.save()
            formContact = ContactForm()
            return render(request,"contact/contacto.html", {"form":formContact, "listadoEnviados":listadoEnviados})
        else:
            log.error("Formulario recibido no pasa la validacion...")
            messages.error(request, "[ERROR]: Algunos campos necesitan llenarse de forma correcta.")
            validErrors(formContact)

    else:
        try:
            emailRecipe = request.GET['emailRecipe'] 
            nameRecipe = request.GET['nameRecipe'] 
            subjectRecipe = request.GET['subjectRecipe']
            descRecipe = request.GET['descRecipe']
            printLogPatients("emailRecipe: "+emailRecipe)
            printLogPatients("nameRecipe: "+nameRecipe)
            printLogPatients("subjectRecipe: "+subjectRecipe)
            printLogPatients("descRecipe: "+descRecipe)
            formContact = ContactForm(request.GET)
        except Exception as ex:
            formContact = ContactForm()
    return render(request,"contact/contacto.html", {"form":formContact, "listadoEnviados":listadoEnviados})


@login_required(login_url=getLogin())
@permission_required(addPatient(),login_url=notPermission())
@validRequest
def altaPaciente(request):
    log.info("[Load view method: altaPaciente]")    
    user = getUser()
    if request.method == 'POST':
        formPatient = PatientForm(request.POST, request.FILES)
        formAdress = AdressForm(request.POST)
        if all([formPatient.is_valid(), formAdress.is_valid()]):
            patient = formPatient.save(commit=False)
            patient.activo = True
            patient.numexp = generateKlave()
            patient.nombre = patient.nombre.title()
            patient.apellidoPaterno = patient.apellidoPaterno.title()
            patient.apellidoMaterno = patient.apellidoMaterno.title()
            patient.email = patient.email.lower()
            patient.fechaAlta = currentLocalTime()
            patient.fechaUpdate = currentLocalTime()
            patient.rfc = patient.rfc.upper()
            patient.userId = userRequest()
            patient.userName = user.get_full_name()
            log.info("Formulario valido, preparando alta de paciente...")
            dataPatient = formPatient.cleaned_data
            printLogPatients("Data recibida del formulario patient: "+str(dataPatient))
            name = dataPatient['nombre']+" "+dataPatient['apellidoPaterno']
       	    patient.save()
            adress = formAdress.save(commit=False)
            adress.patient = patient
            adress.calle = adress.calle.title()
            adress.numeroInt=adress.numeroInt.title()
            adress.numeroExt=adress.numeroExt.title()
            adress.ciudad=adress.ciudad.title()
            adress.estado=adress.estado
            adress.userId = userRequest()
            adress.userName = user.get_full_name()
            
            dataAdress = formAdress.cleaned_data
            printLogPatients("Data recibida del formulario adress: "+str(dataAdress))
            adress.save()

            log.info("Se ha agregado a la BD el nuevo registro")
            messages.success(request, "Los datos han sido agregados correctamente con el expediente: {}".format(patient.numexp))
            return buscarId(request,patient.id)
        else:
            log.error("Formulario recibido no pasa la validacion...")
            messages.error(request, "[ERROR]: Algunos campos necesitan llenarse de forma correcta.")
            validErrors(formPatient)
            validErrors(formAdress)

    else:
        formPatient = PatientForm()
        formAdress = AdressForm()
    return render(request, "patient/alta.html", {"form": formPatient,"formAdress":formAdress})


@login_required(login_url=getLogin())
@permission_required(viewPatient(),login_url=notPermission())
@validRequest
def buscarId(request, idPatient):
    log.info("[Load view method: buscarId(idPatient)]")
    log.info("idPatient: "+str(idPatient))
    formPatient = PatientForm()
    formAdress = AdressForm()
    try:
        result = filterByIdPatient(idPatient,formPatient)
        adress = filterByIdPatientAdress(idPatient,formAdress)

        patient = filterPatientDelete(idPatient)
        if patient:
            delPatient = patient.eliminado
        else:
            delPatient = False

        if adress == None:
            adress = formAdress

        expediente = result.fields['numexp'].initial
        log.info("Expdiente: "+str(expediente))

        return render(request, "patient/datosPaciente.html", {"form": result, "id": idPatient, "formAdress": adress, "expediente": expediente, "delPatient": delPatient})
    except Exception as ex:
        log.error("Error al buscar por id: "+str(ex))
        return render(request,"patient/datosPaciente.html",{"form": None,"formAdress":None})


@login_required(login_url=getLogin())
@permission_required(updatePatient(),login_url=notPermission())
@validRequest
def actualizarPaciente(request,idPatient):
    log.info("[Load view method: actualizarPaciente(idPatient)]")
    log.info("idPatient: "+str(idPatient))
    formPatient = None
    formAdress = None
    expediente = None
    try:
        user = getUser()
        if user.get_username() == 'admin':
            obj = Patient.objects.get(pk=idPatient)
        else:
            obj = Patient.objects.get(pk=idPatient, userId=userRequest())
        expediente = obj.numexp
        try:
            if user.get_username() == 'admin':
                objAdress = Adress.objects.get(patient__pk=idPatient)
            else:
                objAdress = Adress.objects.get(patient__pk=idPatient, userId=userRequest())
        except Exception as ex:
            log.error("Error: "+str(ex))
            objAdress = Adress()
            objAdress.patient = obj
        obj.fechaUpdate = currentLocalTime()
        imageOld = obj.foto
        formPatient = PatientForm(request.POST,request.FILES,instance=obj)
        formAdress = AdressForm(request.POST,instance=objAdress)
        if all([formPatient.is_valid(),formAdress.is_valid()]):
            imageNew = formPatient.cleaned_data.get("foto")
            if imageOld == imageNew:
                printLogPatients("La imagenes son iguales: "+str(imageNew))
            else:
                printLogPatients("Se ha eliminado la imagen vieja: "+str(imageOld))
                printLogPatients("Se añade nueva imagen: "+str(imageNew))
                try:
                    if imageOld:
                        os.remove(settings.MEDIA_PATH+str(imageOld))
                        printLogPatients("Se ha eliminado la imagen: "+str(imageOld))
                except Exception as ex:
                    log.error("No se pudo eliminar la imagen {} por el siguiente error:  {}".format(imageOld,ex))
            log.info("Formulario valido, actualizando datos de paciente...")
            dataPatient = formPatient.cleaned_data
            printLogPatients("Data patient recibida: "+str(dataPatient))

            dataAdress = formAdress.cleaned_data
            printLogPatients("Data adress recibida: "+str(dataAdress))
            formPatient.save()
            dataLoad = Patient.objects.get(pk=idPatient)
            formPatient = PatientForm(instance=dataLoad)
            formAdress.save()

            log.info("Se ha actualizado el registro en BD para el Expediente {}".format(dataPatient['numexp']))
            messages.success(request, "Los datos han sido actualizados correctamente para el expediente: {}".format(dataPatient['numexp']))
            return render(request, "patient/datosPaciente.html", {"form": formPatient, "id": idPatient, "formAdress": formAdress, "expediente": expediente})
        else:
            log.error("Formulario formPatient recibido no pasa la validacion..." +str(formPatient.errors))
            log.error("Formulario formAdress recibido no pasa la validacion..." + str(formAdress.errors))
            validErrors(formPatient)
            validErrors(formAdress)
            return render(request, "patient/datosPaciente.html", {"form": formPatient, "id": idPatient, "formAdress": formAdress, "expediente": expediente})
            ###return buscarId(request, idPatient)
    except Exception as ex:
        log.error("Error: "+str(ex))
        return render(request,"patient/datosPaciente.html",{"form": formPatient,"id":idPatient,"formAdress":formAdress})


@login_required(login_url=getLogin())
@permission_required(deletePatient(),login_url=notPermission())
@validRequest
def eliminarPaciente(request,idPatient):
    log.info("[Load view method: eliminarPaciente(idPatient)]")
    log.info("idPatient: "+str(idPatient))
    try:
        user = getUser()
        if user.get_username() == 'admin':
            patient = Patient.objects.get(pk=idPatient)
        else:
            patient = Patient.objects.get(pk=idPatient, userId=userRequest())
        imageOld = patient.foto
        numexp = patient.numexp
        patient.eliminado = True
        patient.foto = ''
        patient.save()
        log.info("Se ha eliminado el registro de BD con NumExp: {}".format(numexp))
        try:
            if imageOld:
                os.remove(settings.MEDIA_PATH+str(imageOld))
                printLogPatients("Se ha eliminado la imagen: "+str(imageOld))
        except Exception as ex:
            log.error("No se pudo eliminar la imagen {} por el siguiente error:  {}".format(imageOld,ex))
        return render(request, "patient/eliminarPaciente.html", {"exp": numexp})
    except Exception as ex:
        log.error("Error: "+str(ex))
        return render(request,"patient/eliminarPaciente.html",{"exp": None})


@login_required(login_url=getLogin())
@permission_required(viewAdress(), login_url=notPermission())
@validRequest
def listarDireccion(request):
    log.info("[Load view method: listarDireccion]")
    log.info("Obteniendo lista de direcciones")    
    listadoDirecciones = Adress.objects.filter(filterQuery()).order_by('-patient__pk')[:settings.MAX_ROWS_QUERY_MODEL]
    return render(request, "adress/listaDirecciones.html", {"listaDireccion": listadoDirecciones})


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
            file.nombre = file.nombre.capitalize()
            file.userId = userRequest()
            file.userName = user.get_full_name()
            log.info("Formulario valido, preparando alta de archivo...")
            dataFile = formFile.cleaned_data
            printLogPatients("Data recibida del formulario archivo: "+str(dataFile))
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
        fileN = file.path.name.split("/")[1]
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
        messages.error(request, f"[ERROR]: {str(ex)}")
        return render(request, "file/listaArchivos.html", {"listaArchivo": listadoArchivos})


@login_required(login_url=getLogin())
@permission_required(listNavigation(), login_url=notPermission())
@validRequest
def listarNavegacion(request):
    log.info("[Load view method: listarNavegacion]")
    log.info("Obteniendo lista de navegacion")    
    listadoNavegacion = Navigation.objects.filter(filterQuery()).order_by('-eventTime')[:settings.MAX_ROWS_QUERY_MODEL]
    return render(request, "navigation/listaNavegacion.html", {"listaNavegacion": listadoNavegacion})


@login_required(login_url=getLogin())
@permission_required(importFile(), login_url=notPermission())
@validRequest
def importPatients(request):
    log.info("[Load view method: importPatients]")
    log.info("Obteniendo lista de importación")    
    listadoImportacion = Import.objects.filter(
        tipoSubida='Fichero de pacientes').filter(filterQuery()).order_by('-fechaSubida')[:settings.MAX_ROWS_QUERY_MODEL]

    if request.method == 'POST':
        user = getUser()
        importFile = ImportForm(request.POST, request.FILES)
        if importFile.is_valid():
            file = importFile.save(commit=False)
            file.fechaSubida = currentLocalTime()
            fileName = file.path.name
            file.tipoSubida = 'Fichero de pacientes'
            log.info("Formulario valido, preparando sudiba de archivo...")
            dataFile = importFile.cleaned_data
            printLogPatients("Data recibida del formulario archivo: "+str(dataFile))
            file.save()

            xls = pd.read_excel(settings.MEDIA_PATH+str(file.path), skiprows=1)
            xlsValues = xls.values

            headers = list(xls.columns.values)
            printLogPatients("Columns contains in excel: "+str(headers))
            validXSL = False
            if "Nombre" in headers[0]:
                if "Apellido" in headers[1]:
                    if "RFC" in headers[6]:
                        validXSL = True
                        log.info("Excel validado")
            if not validXSL:
                log.info("Excel no validado!!")

            lista = len(xlsValues)
            if lista > 0 and validXSL:
                fila = 0
                for row in xlsValues:
                    fila+=1
                    containsError = guardarPatientXLS(row,userRequest(),fila)
                    if containsError:
                        file.importado = False
                        file.userId = userRequest()
                        file.userName = user.get_full_name()
                        file.save()
                        importFile = ImportForm()
                        log.info("Existen errores de validacion, revisar archivo")
                        messages.error(request, f"[ERROR]: El archivo {fileName} contiene errores o le faltan campos por cumplimentar.")
                        return render(request, "import/importarPaciente.html", {"form": importFile, "listadoImportacion":listadoImportacion})
                    file.importado = True
                    file.userId = userRequest()
                    file.userName = user.get_full_name()
                    file.save()
            else:
                file.importado = False
                file.userId = userRequest()
                file.userName = user.get_full_name()
                file.save()
                importFile = ImportForm()
                log.info("Existen errores de validacion, revisar archivo")
                messages.error(request, f"[ERROR]: El archivo {fileName} debe contener al menos un registro")
                return render(request, "import/importarPaciente.html", {"form": importFile,"listadoImportacion":listadoImportacion})

            log.info("Se ha agregado a la BD el nuevo archivo importado")
            messages.success(
                request, f"El archivo {fileName} ha sido importado correctamente")
            importFile = ImportForm()
            return render(request, "import/importarPaciente.html", {"form": importFile,"listadoImportacion":listadoImportacion})
        else:
            log.error("Formulario recibido no pasa la validacion...")
            validErrors(importFile)
    else:
        importFile = ImportForm()
    return render(request, "import/importarPaciente.html", {"form": importFile, "listadoImportacion": listadoImportacion})


def guardarPatientXLS(row,userId,fila):
    log.info("[Load view method: guardarPatientXLS]")
    user = getUser()
    try:
        patient = Patient()
        patient.numexp = generateKlave()
        patient.nombre = row[0].title()
        patient.apellidoPaterno = row[1].title()
        patient.userId = userId
        patient.userName = user.get_full_name()

        try:
            try:
                patient.apellidoMaterno = row[2].title()
            except:
                log.error("No se encontro >>> Apellido Materno en la [fila,columna]: [{},{}]".format(fila,'3'))
            try:
                patient.email = row[3].lower()
            except:
                log.error("No se encontro >>> Email en la [fila,columna]: [{},{}]".format(fila,'4'))
            try:
                patient.telefono = int(row[4])
            except:
                log.error("No se encontro >>> Telefono en la [fila,columna]: [{},{}]".format(fila,'5'))
            try:
                if row[5].upper() == 'ACTIVO':
                    patient.activo = True
                else:
                    patient.activo = False
            except:
                log.error("No se encontro >>> Estado en la [fila,columna]: [{},{}]".format(fila,'6'))
            try:
                patient.rfc = row[6].upper()
            except:
                log.error("No se encontro >>> RFC en la [fila,columna]: [{},{}]".format(fila,'7'))
        except Exception as error:
            patient.apellidoMaterno = ''
            patient.email = ''
            patient.telefono = ''
            patient.rfc = ''
            log.error("Error: algunos campos no tienen valores en el xls, pero no son obligatorios")

        patient.fechaUpdate = currentLocalTime()
        printLogPatients("Data recibida del xls patient: "+str(patient))
        patient.save()
        
        address = Adress()
        address.patient = patient        
        address.userId = userId
        address.userName = user.get_full_name()
        address.save()

        return False
    except Exception as ex:
        log.error("Error: "+str(ex))
        return True

def validCellValue(val):
    log.info("[Load view method: validCellValue]")
    if pd.isnull(val) == True:
        return True
    else:
        return False


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
            printLogPatients("Data recibida del formulario Task: "+str(dataTask))
            task.save()

            log.info("Se ha agregado a la BD el nuevo registro")

            messages.success(request, f"La tarea {task.nameTask} ha sido agregada correctamente")
            return buscarTaskId(request, task.id)
        else:
            log.error("Formulario recibido no pasa la validacion...")
            messages.error(request, "[ERROR]: Algunos campos necesitan llenarse de forma correcta.")
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
def emailPatient(request, idPatient):
    log.info("[Load view method: emailPatient(idPatient)]")
    log.info("idPatient for email: "+str(idPatient))
    user = getUser()
    if user.get_username() == 'admin':
        patient = Patient.objects.get(pk=idPatient)
    else:
        patient = Patient.objects.get(pk=idPatient, userId=userRequest())

    if not request.GET._mutable:
        request.GET._mutable = True
        request.GET['emailRecipe'] = patient.email
        request.GET['nameRecipe'] = patient.nombre +' '+ patient.apellidoPaterno
        request.GET['subjectRecipe'] = 'Receta de paciente con expediente '+str(patient.numexp)
        request.GET['descRecipe'] = 'A continuación se describe la receta:\n\n'

    return contactoPaciente(request)

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
            printLogPatients("Data task recibida: "+str(dataTask))
            formTask.save()            

            log.info("Se ha actualizado el registro en BD para la tarea {}".format(dataTask['nameTask']))
            messages.success(request, "Los datos han sido actualizados correctamente")
            return buscarTaskId(request, idTask)
        else:
            log.error("Formulario recibido no pasa la validacion...")
            validErrors(formTask)
            return buscarTaskId(request, idTask)
    except Exception as ex:
        log.error("Error: "+str(ex))
        return render(request, "task/detailTask.html", {"form": formTask, "idTask": idTask})

def jsonPatient(request):
    log.info("Load json for get list patient")
    listPatient = Patient.objects.all().order_by('-fechaAlta')[:1000]
    for pa in listPatient:
        log.info(pa)
    listJson = json.dumps([{
        'id': p.id,
        'nombre': p.nombre, 
        'apellidoPaterno':p.apellidoPaterno, 
        'apellidoMaterno': p.apellidoMaterno,
        'numexp':p.numexp,
        'email':p.email,
        'rfc':p.rfc,
        'estado':p.activo,
        'telefono': p.telefono,} for p in listPatient])
    return HttpResponse(listJson, content_type='application/json')


def addContact(request):
    if request.method == 'POST':
        log.info("Method POST with params: "+str(request.POST))
        for p in request.POST:
            log.info("field: {}, value: {}".format(p, request.POST.get(p)))
        data = json.dumps({'result': '¡Add contact OK!'})
        return HttpResponse(data, content_type='application/json')

def updateClassMenu(request):
    try:
        if request.method == 'POST':
            log.debug("Method POST with params: "+str(request.POST))
            for p in request.POST:
                log.debug("field: {}, value: {}".format(p, request.POST.get(p)))
            if request.POST.get('classMenu') != None:
                updatePropertie(userRequest(), 'class_menu', request.POST.get('classMenu'))
                loadPropertie(userRequest(), request)
            data = json.dumps({'result': 'OK'})
            return HttpResponse(data, content_type='application/json')
    except:
        data = json.dumps({'result': 'KO'})
        return HttpResponse(data, content_type='application/json')

def printLogPatients(register):
    log.debug(register)

def userRequest():
    user = getUser()
    return user.id