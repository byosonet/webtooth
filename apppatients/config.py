from webtooth.config import logger
log = logger('apppatients.config', False)

def validErrors(form):
	for field in form.errors:
		form[field].field.widget.attrs['class'] += ' border-bottom-danger'

def addClass(attrs,cclass):
	attrs.update({'class':cclass})
	return attrs

def addPlaceHolder(attrs,name):
	attrs.update({'placeholder':name})
	return attrs

def addStyle(attrs,cstyle):
	attrs.update({'style':cstyle})
	return attrs

def addTextArea(attrs,rows,cols):
	attrs.update({'rows':rows})
	attrs.update({'cols':cols})
	return attrs

def inputCSS(name):
	attrs={}
	attrs=addClass(attrs,'form-control form-control-user')
	attrs=addPlaceHolder(attrs,name)
	attrs = tooltip(attrs, name)
	log.info("input: "+str(attrs))
	return attrs

def selectCSS(name):
	attrs={}
	attrs = addClass(attrs, 'form-control custom-select custom-select-sm')
	attrs=addPlaceHolder(attrs,name)
	attrs = tooltip(attrs, name)
	log.info("select: "+str(attrs))
	return attrs

def addMaxLength(attrs,max):
	attrs.update({'maxlength':max})
	return attrs


def addHidden(attrs):
	attrs.update({'type': 'hidden'})
	return attrs

def textAreaCSS(placeHolder):
	attrs={}
	attrs=addClass(attrs,'form-control')
	attrs=addPlaceHolder(attrs, placeHolder)
	attrs=addTextArea(attrs,14,20)
	attrs=addStyle(attrs,'overflow:auto;resize:none')
	attrs=addMaxLength(attrs,3500)
	attrs = tooltip(attrs, placeHolder)
	log.info("textArea: "+str(attrs))
	return attrs

def addReadOnly(attrs):
	attrs.update({'readonly':True})
	return attrs

def customInputReadOnly(name):
	attrs = {}
	attrs=addClass(attrs,'form-control form-control-user')
	attrs=addPlaceHolder(attrs,name)
	attrs=addReadOnly(attrs)
	attrs = addHidden(attrs)
	log.info("input: "+str(attrs))
	return attrs

def imageCSS(name):
	attrs = {'accept': 'image/jpeg'}
	attrs = addClass(attrs, 'btn btn-secondary btn-user')
	attrs = tooltip(attrs, name)
	log.info("imageCSS: " +str(attrs))
	return attrs

def fileCSS(name):
	attrs = {'accept': '*'}
	attrs = addClass(attrs, 'btn btn-secondary btn-user')
	attrs = tooltip(attrs, name)
	log.info("fileCSS: " + str(attrs))
	return attrs


def xlsCSS(name):
	attrs = {'accept': 'application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
	attrs = addClass(attrs, 'btn btn-secondary btn-user')
	attrs = tooltip(attrs, name)
	log.info("xlsCSS: " + str(attrs))
	return attrs

def tooltip(attrs, title):
	attrs.update({'data-placement': 'top'})
	attrs.update({'data-trigger': 'hover'})
	attrs.update({'rel': 'popover'})
	attrs.update({'data-original-title': title})
	attrs.update({'data-content': title})
	
	log.info("tooltip: "+str(attrs))
	return attrs

def inputReadOnly(name):
	attrs = {}
	attrs = addClass(attrs, 'form-control form-control-user')
	attrs = addPlaceHolder(attrs, name)
	attrs = tooltip(attrs, name)
	attrs = addReadOnly(attrs)
	log.info("inputReadOnly: "+str(attrs))
	return attrs

OPTIONS_ESTADO = (
	("", "Selecciona un estado"),
	("Aguascalientes","Aguascalientes"),
    ("Baja California", "Baja California"),
    ("Baja California Sur","Baja California Sur"),
    ("Chihuahua","Chihuahua"),
    ("Chiapas","Chiapas"),
    ("Campeche","Campeche"),
    ("Ciudad de México","Ciudad de México"),
    ("Coahuila","Coahuila"),
    ("Colima","Colima"),
    ("Durango","Durango"),
    ("Guerrero","Guerrero"),
    ("Guanajuato","Guanajuato"),
    ("Hidalgo","Hidalgo"),
    ("Jalisco","Jalisco"),
    ("Michoacán","Michoacán"),
    ("Estado de México","Estado de México"),
    ("Morelos","Morelos"),
    ("Nayarit","Nayarit"),
    ("Nuevo León","Nuevo León"),
    ("Oaxaca","Oaxaca"),
    ("Puebla","Puebla"),
    ("Quintana Roo","Quintana Roo"),
    ("Querétaro","Querétaro"),
    ("Sinaloa","Sinaloa"),
    ("San Luis Potosí","San Luis Potosí"),
    ("Sonora","Sonora"),
    ("Tabasco","Tabasco"),
    ("Tlaxcala","Tlaxcala"),
    ("Tamaulipas","Tamaulipas"),
    ("Veracruz","Veracruz"),
    ("Yucatán","Yucatán"),
    ("Zacatecas","Zacatecas")
	)

OPTIONS_SEXO = (
    ("", "Selecciona sexo"),
   	("Masculino", "Masculino"),
    ("Femenino", "Femenino")
)
