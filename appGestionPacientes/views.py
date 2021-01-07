from appGestionPacientes import urls
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

import os
from django.conf import settings

from appGestionPacientes.models import Patient, Adress, File, Navigation
from appGestionPacientes.forms import ContactForm, PatientForm, AdressForm, FileForm, ImportForm
from appGestionPacientes.config import validErrors
from appGestionPacientes.query import filterSearch, filterByIdPatient, generateKlave, filterByIdPatientAdress

from webtooth.config import logger, sendEmailContact, getLogin
from appGestionPacientes.permissions import *
from webtooth.decorators import validRequest
from django.contrib import messages

import pandas as pd

log = logger('appGestionPacientes',True)

@login_required(login_url=getLogin())
@validRequest
def buscarPaciente(request):
    log.info("Buscando paciente")
    return render(request,"patient/buscarPaciente.html")

@login_required(login_url=getLogin())
@permission_required(viewPatient(),login_url=notPermission())
@validRequest
def buscarNombre(request):
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
    log.info("Obteniendo lista de pacientes")
    listadoPacientes = Patient.objects.all().order_by('-fechaUpdate')
    #for p in listadoPacientes:
        #log.info("Nombre: {} Expediente: {} Correo: {} Fecha update: {}".format(p.nombre,p.numexp,p.email,p.fechaUpdate))    
    return render(request, "patient/listaPacientes.html", {"listaPaciente":listadoPacientes})

@login_required(login_url=getLogin())
@validRequest
def contactoPaciente(request):
    if request.method=='POST':
        formContact = ContactForm(request.POST)
        if formContact.is_valid():
            log.info("Formulario valido, preparando envío...")
            dataContact = formContact.cleaned_data
            email=sendEmailContact(dataContact)
            if email == None:
                messages.error(
                    request, f"Servidor de correo no disponible, intentelo más tarde.")
            else:
                messages.success(request, f"El correo se ha enviado correctamente ha: {email}")
            formContact = ContactForm()
            return render(request,"contact/contacto.html", {"form":formContact})
        else:
            log.error("Formulario recibido no pasa la validacion...")
            messages.error(request, "[ERROR]: Algunos campos necesitan llenarse de forma correcta.")
            validErrors(formContact)

    else:
        formContact = ContactForm()
    return render(request,"contact/contacto.html", {"form":formContact})


@login_required(login_url=getLogin())
@permission_required(addPatient(),login_url=notPermission())
@validRequest
def altaPaciente(request):
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
            patient.rfc = patient.rfc.upper()
            log.info("Formulario valido, preparando alta de paciente...")
            dataPatient = formPatient.cleaned_data
            log.info("Data recibida del formulario patient: "+str(dataPatient))
            name = dataPatient['nombre']+" "+dataPatient['apellidoPaterno']
       	    patient.save()
            adress = formAdress.save(commit=False)
            adress.patient = patient
            adress.calle = adress.calle.title()
            adress.numeroInt=adress.numeroInt.title()
            adress.numeroExt=adress.numeroExt.title()
            adress.ciudad=adress.ciudad.title()
            adress.estado=adress.estado
            
            dataAdress = formAdress.cleaned_data
            log.info("Data recibida del formulario adress: "+str(dataAdress))
            adress.save()

            log.info("Se ha agregado a la BD el nuevo registro")
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
@validRequest
def buscarId(request, idPatient):
    formPatient = PatientForm()
    formAdress = AdressForm()
    try:
        result = filterByIdPatient(idPatient,formPatient)
        adress = filterByIdPatientAdress(idPatient,formAdress)

        if adress == None:
            adress = formAdress

        expediente = result.fields['numexp'].initial
        log.info("Expdiente: "+str(expediente))

        return render(request, "patient/datosPaciente.html", {"form": result, "id": idPatient, "formAdress": adress, "expediente": expediente})
    except Exception as ex:
        log.error("Error al buscar por id: "+str(ex))
        return render(request,"patient/datosPaciente.html",{"form": None,"formAdress":None})


@login_required(login_url=getLogin())
@permission_required(updatePatient(),login_url=notPermission())
@validRequest
def actualizarPaciente(request,idPatient):
    log.info("id: "+str(idPatient))
    formPatient = None
    formAdress = None
    try:
        obj = Patient.objects.get(pk=idPatient)
        try:
            objAdress = Adress.objects.get(patient__pk=idPatient)
        except Exception as ex:
            log.error("Error: "+str(ex))
            objAdress = Adress()
            objAdress.patient = obj
        obj.fechaUpdate=timezone.now()
        imageOld = obj.foto
        formPatient = PatientForm(request.POST,request.FILES,instance=obj)
        formAdress = AdressForm(request.POST,instance=objAdress)
        if all([formPatient.is_valid(),formAdress.is_valid()]):
            imageNew = formPatient.cleaned_data.get("foto")
            if imageOld == imageNew:
                log.info("La imagenes son iguales: "+str(imageNew))
            else:
                log.info("Se ha eliminado la imagen vieja: "+str(imageOld))
                log.info("Se añade nueva imagen: "+str(imageNew))
                try:
                    if imageOld:
                        os.remove(settings.MEDIA_PATH+str(imageOld))
                        log.info("Se ha eliminado la imagen: "+str(imageOld))
                except Exception as ex:
                    log.error("No se pudo eliminar la imagen {} por el siguiente error:  {}".format(imageOld,ex))
            log.info("Formulario valido, actualizando datos de paciente...")
            dataPatient = formPatient.cleaned_data
            log.info("Data patient recibida: "+str(dataPatient))

            dataAdress = formAdress.cleaned_data
            log.info("Data adress recibida: "+str(dataAdress))
            formPatient.save()
            formAdress.save()
            
            expediente = dataPatient['numexp']

            log.info("Se ha actualizado el registro en BD para el Expediente {}".format(dataPatient['numexp']))
            messages.success(request, "Los datos han sido actualizados correctamente para el expediente: {}".format(dataPatient['numexp']))
            return render(request, "patient/datosPaciente.html", {"form": formPatient, "id": idPatient, "formAdress": formAdress, "expediente": expediente})
        else:
            log.error("Formulario recibido no pasa la validacion...")
            validErrors(formPatient)
            validErrors(formAdress)
            return render(request,"patient/datosPaciente.html",{"form": formPatient,"id":idPatient,"formAdress":formAdress})
    except Exception as ex:
        log.error("Error: "+str(ex))
        return render(request,"patient/datosPaciente.html",{"form": formPatient,"id":idPatient,"formAdress":formAdress})


@login_required(login_url=getLogin())
@permission_required(deletePatient(),login_url=notPermission())
@validRequest
def eliminarPaciente(request,idPatient):
    log.info("ID recibido: "+str(idPatient))
    try:
        patient = Patient.objects.get(pk=idPatient)
        imageOld = patient.foto
        numexp = patient.numexp
        patient.delete()
        log.info("Se ha eliminado el registro de BD con NumExp: {}".format(numexp))
        try:
            if imageOld:
                os.remove(settings.MEDIA_PATH+str(imageOld))
                log.info("Se ha eliminado la imagen: "+str(imageOld))
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
    log.info("Obteniendo lista de direcciones")
    listadoDirecciones = Adress.objects.all().order_by('-patient__pk')
    for d in listadoDirecciones:
       log.info("Calle: {} Ciudad: {} Estado: {} Numexp: {}".format(d.calle,d.ciudad,d.estado,d.patient.numexp))
    return render(request, "adress/listaDirecciones.html", {"listaDireccion": listadoDirecciones})


@login_required(login_url=getLogin())
@permission_required(addFile(), login_url=notPermission())
@validRequest
def altaArchivo(request):
    if request.method == 'POST':
        formFile = FileForm(request.POST, request.FILES)
        if formFile.is_valid():
            file = formFile.save(commit=False)
            file.fechaSubida = timezone.now()
            fileName = file.nombre+"."+file.path.name.split(".")[1]
            file.path.name = fileName
            file.nombre = file.nombre.capitalize()
            log.info("Formulario valido, preparando alta de archivo...")
            dataFile = formFile.cleaned_data
            log.info("Data recibida del formulario archivo: "+str(dataFile))
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
    log.info("Obteniendo lista de archivos")
    listadoArchivos = File.objects.all().order_by('-fechaSubida')
    for file in listadoArchivos:
       log.info("Nombre: {} Path: {}".format(file.nombre, file.path))
    return render(request, "file/listaArchivos.html", {"listaArchivo": listadoArchivos})


@login_required(login_url=getLogin())
@permission_required(deleteFile(), login_url=notPermission())
@validRequest
def eliminarArchivo(request, idFile):
    listadoArchivos = File.objects.all().order_by('-fechaSubida')
    try:
        log.info("ID File recibido: "+str(idFile))
        file = File.objects.get(pk=idFile)
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
    log.info("Obteniendo lista de navegacion")
    listadoNavegacion = Navigation.objects.all().order_by('-eventTime')[:200]
    return render(request, "navigation/listaNavegacion.html", {"listaNavegacion": listadoNavegacion})


@login_required(login_url=getLogin())
@permission_required(importFile(), login_url=notPermission())
@validRequest
def importPatients(request):
    if request.method == 'POST':
        importFile = ImportForm(request.POST, request.FILES)
        if importFile.is_valid():
            file = importFile.save(commit=False)
            file.fechaSubida = timezone.now()
            fileName = file.path.name
            file.tipoSubida = 'Fichero de pacientes'
            log.info("Formulario valido, preparando sudiba de archivo...")
            dataFile = importFile.cleaned_data
            log.info("Data recibida del formulario archivo: "+str(dataFile))
            file.save()

            xls = pd.read_excel(settings.MEDIA_PATH+str(file.path), skiprows=1)
            xlsValues = xls.values

            lista = len(xlsValues)
            if lista > 0:
                for row in xlsValues:
                    containsError = guardarPatientXLS(row)
                    if containsError:
                        importFile = ImportForm()
                        log.info("Existen errores de validacion, revisar archivo")
                        messages.error(request, f"[ERROR]: El archivo {fileName} contiene errores o le faltan campos por cumplimentar.")
                        return render(request, "import/importarPaciente.html", {"form": importFile})
            else:
                importFile = ImportForm()
                log.info("Existen errores de validacion, revisar archivo")
                messages.error(request, f"[ERROR]: El archivo {fileName} debe contener al menos un registro")
                return render(request, "import/importarPaciente.html", {"form": importFile})


            log.info("Se ha agregado a la BD el nuevo archivo importado")
            messages.success(
                request, f"El archivo {fileName} ha sido importado correctamente")
            importFile = ImportForm()
            return render(request, "import/importarPaciente.html", {"form": importFile})
        else:
            log.error("Formulario recibido no pasa la validacion...")
            validErrors(importFile)
    else:
        importFile = ImportForm()
    return render(request, "import/importarPaciente.html", {"form": importFile})


def guardarPatientXLS(row):
    try:
        patient = Patient()
        patient.numexp = generateKlave()
        patient.nombre = row[0].title()
        patient.apellidoPaterno = row[1].title()

        try:
            patient.apellidoMaterno = row[2].title()
            patient.email = row[3].lower()
            patient.telefono = row[4]

            if row[5] == 'Activo':
                patient.activo = True
            else:
                patient.activo = False

            patient.rfc = row[6].upper()
        except Exception as error:
            patient.apellidoMaterno = ''
            patient.email = ''
            patient.telefono = ''
            patient.rfc = ''
            log.error("Error: algunos campos no tienen valores en el xls, pero no son obligatorios")

        patient.fechaUpdate = timezone.now()
        log.info("Data recibida del xls patient: "+str(patient))
        patient.save()
        return False
    except Exception as ex:
        log.error("Error: "+str(ex))
        return True

def validCellValue(val):
    if pd.isnull(val) == True:
        return True
    else:
        return False

