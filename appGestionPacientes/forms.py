from django import forms
from appGestionPacientes.config import *
from appGestionPacientes.models import Patient, Adress, File, Import, Task, Recipe


class ContactForm(forms.ModelForm):
	subjectRecipe = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Asunto (*)')))
	emailRecipe = forms.EmailField(widget=forms.EmailInput(attrs=inputCSS('Email (*)')))
	nameRecipe = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre (*)')))
	descRecipe = forms.CharField(widget=forms.Textarea(attrs=textAreaCSS('Receta')))

	class Meta:
		model = Recipe
		fields = ['subjectRecipe', 'emailRecipe', 'nameRecipe', 'descRecipe']


class PatientForm(forms.ModelForm):
	nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre(s)*')))
	apellidoPaterno = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Apellido paterno*')))
	apellidoMaterno = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs=inputCSS('Apellido materno')))
	rfc = forms.CharField(required=False,max_length=13, widget=forms.TextInput(attrs=inputCSS('RFC')))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs=inputCSS('Email')))
	telefono = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs=inputCSS('Teléfono')))
	numexp = forms.CharField(required=False, max_length=15, widget=forms.TextInput(
		attrs=customInputReadOnly('Número expediente')))
	foto = forms.ImageField(required=False,widget=forms.FileInput(attrs=imageCSS()))
	activo = forms.BooleanField(required=False)

	class Meta:
		model = Patient
		fields = ['nombre', 'apellidoPaterno', 'apellidoMaterno',
                    'email', 'telefono', 'numexp', 'foto', 'activo','rfc']

class AdressForm(forms.ModelForm):
	calle=forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs=inputCSS('Dirección')))
	numeroExt=forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs=inputCSS('Número exterior')))
	numeroInt=forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs=inputCSS('Número interior')))
	ciudad = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs=inputCSS('Ciudad')))
	estado=forms.CharField(required=False, max_length=50, widget=forms.Select(attrs=selectCSS('Estado'),choices=OPTIONS_ESTADO))
	cp=forms.CharField(required=False, max_length=6, widget=forms.TextInput(attrs=inputCSS('C.P.')))

	class Meta:
		model = Adress
		fields = ['calle','numeroExt','numeroInt','ciudad','estado','cp']


class FileForm(forms.ModelForm):
	nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre del archivo (*)')))
	path = forms.FileField(widget=forms.FileInput(attrs=fileCSS()))

	class Meta:
		model = File
		fields = ['nombre', 'path']


class ImportForm(forms.ModelForm):
	path = forms.FileField(widget=forms.FileInput(attrs=xlsCSS()))

	class Meta:
		model = Import
		fields = ['path']


class TaskForm(forms.ModelForm):
	nameTask = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre de la tarea (*)')))
	descTask = forms.CharField(required=True, widget=forms.Textarea(attrs=textAreaCSS('Descripción de la tarea (*)')))
	status = forms.BooleanField(required=False)
	dateCreate = forms.DateTimeField(required=True, widget=forms.TextInput(attrs=inputCSS('Fecha programada')))

	class Meta:
		model = Task
		fields = ['nameTask', 'descTask', 'status', 'dateCreate']
