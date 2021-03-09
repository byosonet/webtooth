from webtooth.config import logger
log = logger('apptasks.config', False)

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
	printElement("input: "+str(attrs))
	return attrs

def addMaxLength(attrs,max):
	attrs.update({'maxlength':max})
	return attrs

def textAreaCSS(placeHolder):
	attrs={}
	attrs=addClass(attrs,'form-control')
	attrs=addPlaceHolder(attrs, placeHolder)
	attrs=addTextArea(attrs,14,20)
	attrs=addStyle(attrs,'overflow:auto;resize:none')
	attrs=addMaxLength(attrs,3500)
	attrs = tooltip(attrs, placeHolder)
	printElement("textArea: "+str(attrs))
	return attrs

def tooltip(attrs, title):
	attrs.update({'data-placement': 'top'})
	attrs.update({'data-trigger': 'hover'})
	attrs.update({'rel': 'popover'})
	attrs.update({'data-original-title': title})
	attrs.update({'data-content': title})
	
	printElement("tooltip: "+str(attrs))
	return attrs

def printElement(element):
	log.debug(element)

