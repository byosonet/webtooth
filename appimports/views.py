from django.contrib.auth.decorators import login_required, permission_required
from webtooth.decorators import validRequest
from django.shortcuts import render
from django.conf import settings

from . models import Import
from . forms import ImportForm
from . config import validErrors

from apppatients.models import Patient, Adress
from apppatients.query import generateKlave
from appimports.permissions import *
from webtooth.config import logger, getLogin, currentLocalTime, filterQuery
from django.contrib import messages
from webtooth.signals import getUser

import pandas as pd

# Create your views here.
log = logger('appimports', True)

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
            printLogImports("Data recibida del formulario archivo: "+str(dataFile))
            file.save()

            xls = pd.read_excel(settings.MEDIA_PATH+str(file.path), skiprows=1)
            xlsValues = xls.values

            headers = list(xls.columns.values)
            printLogImports("Columns contains in excel: "+str(headers))
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
                        messages.error(request, f"¡El archivo {fileName} contiene errores o le faltan campos por cumplimentar!")
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
                messages.error(request, f"¡El archivo {fileName} debe contener al menos un registro!")
                return render(request, "import/importarPaciente.html", {"form": importFile,"listadoImportacion":listadoImportacion})

            log.info("Se ha agregado a la BD el nuevo archivo importado")
            messages.success(
                request, f"¡El archivo {fileName} ha sido importado correctamente!")
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
        printLogImports("Data recibida del xls patient: "+str(patient))
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

def userRequest():
    user = getUser()
    return user.id

def printLogImports(register):
    log.debug(register)