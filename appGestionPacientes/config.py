from webtooth.config import logger
log = logger('appGestionPacientes.config',False)

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
	log.info("input: "+str(attrs))
	return attrs

def selectCSS(name):
	attrs={}
	attrs=addClass(attrs,'form-control')
	attrs=addPlaceHolder(attrs,name)
	log.info("select: "+str(attrs))
	return attrs

def addMaxLength(attrs,max):
	attrs.update({'maxlength':max})
	return attrs

def textAreaCSS(placeHolder):
	attrs={}
	attrs=addClass(attrs,'form-control')
	attrs=addPlaceHolder(attrs, placeHolder)
	attrs=addTextArea(attrs,15,20)
	attrs=addStyle(attrs,'overflow:auto;resize:none')
	attrs=addMaxLength(attrs,3500)
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
	log.info("input: "+str(attrs))
	return attrs

def imageCSS():
	attrs = {'accept': 'image/jpeg'}
	attrs = addClass(attrs, 'btn btn-secondary btn-user')
	log.info("imageCSS: " +str(attrs))
	return attrs

def fileCSS():
	attrs = {'accept': '*'}
	attrs = addClass(attrs, 'btn btn-secondary btn-user')
	log.info("fileCSS: " + str(attrs))
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