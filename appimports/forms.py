from django import forms
from appimports.config import xlsCSS
from appimports.models import Import

class ImportForm(forms.ModelForm):
	path = forms.FileField(widget=forms.FileInput(attrs=xlsCSS('Seleccionar excel')))

	class Meta:
		model = Import
		fields = ['path']