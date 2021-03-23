from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings

from . models import Recipe
from . forms import ContactForm

from apppatients.models import Patient
from apprecipes.config import validErrors

from webtooth.config import logger, sendEmailContact, getLogin, filterQuery
from apprecipes.permissions import *
from webtooth.decorators import validRequest
from django.contrib import messages
from webtooth.signals import getUser

# Create your views here.
log = logger('apprecipes', True)

@login_required(login_url=getLogin())
@permission_required(addRecipe(),login_url=notPermission())
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
            printLogRecipes("Data recibida del formulario Recipe: "+str(dataContact))
            log.info("Se ha agregado a la BD el nuevo registro")
            
            email=sendEmailContact(dataContact)
            if email == None:
                recipe.stateRecipe = 'No enviado'
                messages.error(
                    request, f"¡Servidor de correo no disponible, intentelo más tarde!")
            else:
                recipe.stateRecipe = 'Enviado'
                messages.success(request, f"¡El correo se ha enviado correctamente ha: {email}!")
            recipe.save()
            return redirect("contactoPaciente")
        else:
            log.error("Formulario recibido no pasa la validacion...")
            messages.error(request, "¡Algunos campos necesitan llenarse de forma correcta!")
            validErrors(formContact)

    else:
        try:
            emailRecipe = request.GET['emailRecipe'] 
            nameRecipe = request.GET['nameRecipe'] 
            subjectRecipe = request.GET['subjectRecipe']
            descRecipe = request.GET['descRecipe']
            printLogRecipes("emailRecipe: "+emailRecipe)
            printLogRecipes("nameRecipe: "+nameRecipe)
            printLogRecipes("subjectRecipe: "+subjectRecipe)
            printLogRecipes("descRecipe: "+descRecipe)
            formContact = ContactForm(request.GET)
        except Exception as ex:
            log.error("Error: "+str(ex))
            formContact = ContactForm()
    return render(request,"contact/contacto.html", {"form":formContact, "listadoEnviados":listadoEnviados})

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

def printLogRecipes(register):
    log.debug(register)

def userRequest():
    user = getUser()
    return user.id