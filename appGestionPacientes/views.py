from appGestionPacientes import urls
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

import os
from django.conf import settings

from appGestionPacientes.models import Patient, Adress, File, Navigation
from appGestionPacientes.forms import ContactForm, PatientForm, AdressForm, FileForm
from appGestionPacientes.config import validErrors
from appGestionPacientes.query import filterSearch, filterByIdPatient, generateKlave, filterByIdPatientAdress

from webtooth.config import logger, sendEmailContact, getLogin
from appGestionPacientes.permissions import *
from webtooth.decorators import validRequest

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
            return render(request,"contact/enviado.html",{"correo":email})
        else:
            log.error("Formulario recibido no pasa la validacion...")
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
            adress.estado=adress.estado.title()
            
            dataAdress = formAdress.cleaned_data
            log.info("Data recibida del formulario adress: "+str(dataAdress))
            adress.save()

            log.info("Se ha agregado a la BD el nuevo registro")
            return render(request, "patient/altaEnviada.html", {"nombre": name})
        else:
            log.error("Formulario recibido no pasa la validacion...")
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

        return render(request,"patient/datosPaciente.html",{"form": result,"id":idPatient,"formAdress":adress})
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
        objAdress = Adress.objects.get(patient__pk=idPatient)
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
                        os.remove(settings.MEDIA_REMOVE+str(imageOld))
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
            
            log.info("Se ha actualizado el registro en BD para el Expediente {}".format(dataPatient['numexp']))
            return render(request, "patient/datosPacienteEnviada.html", {"exp": dataPatient['numexp'],"idPatient":idPatient})
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
                os.remove(settings.MEDIA_REMOVE+str(imageOld))
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
            file.descripcion = file.descripcion.capitalize()
            file.nombre = file.nombre.capitalize()
            log.info("Formulario valido, preparando alta de archivo...")
            dataFile = formFile.cleaned_data
            log.info("Data recibida del formulario archivo: "+str(dataFile))
            file.save()            
            log.info("Se ha agregado a la BD el nuevo registro de archivo")
            return render(request, "file/altaArchivoEnviada.html", {"nombre": fileName})
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
    try:
        log.info("ID File recibido: "+str(idFile))
        file = File.objects.get(pk=idFile)
        fileOld = file.path
        log.info("Se ha eliminado el archivo de BD: {}".format(file.fileName))
        file.delete()
        try:
            if fileOld:
                os.remove(settings.MEDIA_REMOVE+str(fileOld))
                log.info("Se ha eliminado el archivo: "+str(fileOld))
        except Exception as ex:
            log.error("No se pudo eliminar el archivo {} por el siguiente error:  {}".format(
                fileOld, ex))
        return redirect(urls.URL_LISTAR_ARCHIVO)
    except Exception as ex:
        log.error("Error: "+str(ex))
        return redirect(urls.URL_LISTAR_ARCHIVO)


@login_required(login_url=getLogin())
@permission_required(listNavigation(), login_url=notPermission())
@validRequest
def listarNavegacion(request):
    log.info("Obteniendo lista de navegacion")
    listadoNavegacion = Navigation.objects.all().order_by('-eventTime')[:200]
    return render(request, "navigation/listaNavegacion.html", {"listaNavegacion": listadoNavegacion})
