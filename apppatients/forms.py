from django import forms
from apppatients.config import *
from apppatients.models import Patient, Adress
from webtooth.settings import DATE_INPUT_FORMAT, DATE_INPUT_SHOW, DATETIME_INPUT_FORMAT, DATETIME_INPUT_SHOW


class PatientForm(forms.ModelForm):
	nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre(s)*')))
	apellidoPaterno = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Apellido paterno*')))
	apellidoMaterno = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs=inputCSS('Apellido materno')))
	rfc = forms.CharField(required=False,max_length=13, widget=forms.TextInput(attrs=inputCSS('RFC')))
	email = forms.EmailField(required=False, widget=forms.EmailInput(attrs=inputCSS('Email')))
	telefono = forms.CharField(required=False, max_length=10, widget=forms.TextInput(attrs=inputCSS('Teléfono')))
	numexp = forms.CharField(required=False, max_length=15, widget=forms.TextInput(
		attrs=customInputReadOnly('Número expediente')))
	foto = forms.ImageField(required=False,widget=forms.FileInput(attrs=imageCSS('Seleccionar foto')))
	activo = forms.BooleanField(required=False)
	fechaAlta = forms.DateTimeField(input_formats=DATETIME_INPUT_FORMAT, required=False, disabled=True,
	                                widget=forms.DateInput(format=DATETIME_INPUT_SHOW, attrs=inputReadOnly('Fecha de alta')))
	sexo = forms.CharField(required=False, max_length=50, widget=forms.Select(attrs=selectCSS('Sexo'), choices=OPTIONS_SEXO))
	ocupacion = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs=inputCSS('Ocupación')))
	fechaNacimiento = forms.DateTimeField(input_formats=DATE_INPUT_FORMAT, required=False, widget=forms.DateInput(
		format=DATE_INPUT_SHOW, attrs=inputCSS('Fecha nacimiento')))
	fechaUpdate = forms.DateTimeField(input_formats=DATETIME_INPUT_FORMAT, required=False, disabled=True,
                                   widget=forms.DateInput(format=DATETIME_INPUT_SHOW, attrs=inputReadOnly('Fecha de actualizacón')))

	class Meta:
		model = Patient
		fields = ['nombre', 'apellidoPaterno', 'apellidoMaterno',
                    'email', 'telefono', 'numexp', 'foto', 'activo', 'rfc', 'fechaAlta', 'sexo', 'ocupacion', 'fechaNacimiento', 'fechaUpdate']
	
	def clean_email(self):
		log.info("cleaned_data field email to lower!!")
		email = self.cleaned_data['email'].lower()
		return email

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

