
from django import forms
from apptasks.config import inputCSS, textAreaCSS
from apptasks.models import Task
from webtooth.settings import DATETIME_INPUT_FORMAT, DATETIME_INPUT_SHOW

class TaskForm(forms.ModelForm):
	nameTask = forms.CharField(required=True,max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre de la tarea (*)')))
	descTask = forms.CharField(required=True, widget=forms.Textarea(attrs=textAreaCSS('Descripción de la tarea (*)')))
	status = forms.BooleanField(required=False)
	dateCreate = forms.DateTimeField(input_formats=DATETIME_INPUT_FORMAT, required=True, widget=forms.DateInput(
		format=DATETIME_INPUT_SHOW, attrs=inputCSS('Fecha programada (*)')))
	dateExecute = forms.DateTimeField(input_formats=DATETIME_INPUT_FORMAT, required=False, widget=forms.DateInput(
		format=DATETIME_INPUT_SHOW, attrs=inputCSS('Fecha ejecución')))

	class Meta:
		model = Task
		fields = ['nameTask', 'descTask', 'status', 'dateCreate', 'dateExecute']