from django import forms
from apprecipes.config import inputCSS, textAreaCSS
from apprecipes.models import Recipe


class ContactForm(forms.ModelForm):
	subjectRecipe = forms.CharField(max_length=50, widget=forms.TextInput(attrs=inputCSS('Asunto (*)')))
	emailRecipe = forms.EmailField(widget=forms.EmailInput(attrs=inputCSS('Email (*)')))
	nameRecipe = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs=inputCSS('Nombre (*)')))
	descRecipe = forms.CharField(widget=forms.Textarea(attrs=textAreaCSS('Descripción de la receta')))

	class Meta:
		model = Recipe
		fields = ['subjectRecipe', 'emailRecipe', 'nameRecipe', 'descRecipe']
