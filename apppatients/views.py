from apppatients import urls
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from webtooth.config import currentLocalTime,filterQuery, updatePropertie, loadPropertie
from django.http import HttpResponse
import json

import os
from django.conf import settings

from apppatients.models import Patient, Adress
from apppatients.forms import PatientForm, AdressForm
from apppatients.config import validErrors
from apppatients.query import filterSearch, filterByIdPatient, generateKlave, filterByIdPatientAdress, filterPatientDelete

from webtooth.config import logger, sendEmailContact, getLogin, getListTask
from apppatients.permissions import *
from webtooth.decorators import validRequest
from django.contrib import messages
from webtooth.signals import getUser

from apphistory.views import createHistoryGroup, createHistoryStudy, getAllHistoryByPatient
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
    listadoPacientes = filterSearch(request)
    return render(request, "patient/listaPacientes.html", {"listaPaciente":listadoPacientes,"txtbuscado":"No se encontraron datos"})

@login_required(login_url=getLogin())
@permission_required(viewPatient(),login_url=notPermission())
@validRequest
def listarPaciente(request):
    log.info("[Load view method: listarPaciente]")
    log.info("Obteniendo lista de pacientes")    
    listadoPacientes = Patient.objects.filter(filterQuery()).order_by('-fechaUpdate')[:settings.MAX_ROWS_QUERY_MODEL]
    return render(request, "patient/listaPacientes.html", {"listaPaciente":listadoPacientes})

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
        group = createHistoryGroup(request)
        study = createHistoryStudy(request)
        history = getAllHistoryByPatient(request,idPatient)

        patient = filterPatientDelete(idPatient)
        if patient:
            delPatient = patient.eliminado
        else:
            delPatient = False

        if adress == None:
            adress = formAdress

        expediente = result.fields['numexp'].initial
        log.info("Expdiente: "+str(expediente))

        return render(request, "patient/datosPaciente.html", {"form": result, "id": idPatient, "formAdress": adress, "expediente": expediente, "delPatient": delPatient, "group":group,"study":study, "history":history})
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
            dataNombre = formPatient.cleaned_data.get("nombre")
            dataAppaterno = formPatient.cleaned_data.get("apellidoPaterno")
            if dataNombre == None or dataAppaterno == None:
                printLogPatients("El campo nombre/apellido paterno viene vacío, se recarga los datos de patient.")
                return buscarId(request, idPatient)
            return render(request, "patient/datosPaciente.html", {"form": formPatient, "id": idPatient, "formAdress": formAdress, "expediente": expediente})
    except Exception as ex:
        log.error("Error: "+str(ex))
        return buscarId(request, idPatient)


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

def printLogPatients(register):
    log.debug(register)

def userRequest():
    user = getUser()
    return user.id