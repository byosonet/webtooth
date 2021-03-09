from django import forms
from appfiles.config import inputCSS, fileCSS
from appfiles.models import File


class FileForm(forms.ModelForm):
	nombre = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre del archivo (*)')))
	path = forms.FileField(widget=forms.FileInput(attrs=fileCSS('Seleccionar archivo')))

	class Meta:
		model = File
		fields = ['nombre', 'path']