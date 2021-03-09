from webtooth.config import logger
log = logger('appfiles.config', False)

def validErrors(form):
	for field in form.errors:
		form[field].field.widget.attrs['class'] += ' border-bottom-danger'

def addClass(attrs,cclass):
	attrs.update({'class':cclass})
	return attrs

def addPlaceHolder(attrs,name):
	attrs.update({'placeholder':name})
	return attrs

def inputCSS(name):
	attrs={}
	attrs=addClass(attrs,'form-control form-control-user')
	attrs=addPlaceHolder(attrs,name)
	attrs = tooltip(attrs, name)
	printElement("input: "+str(attrs))
	return attrs

def fileCSS(name):
	attrs = {'accept': '*'}
	attrs = addClass(attrs, 'btn btn-secondary btn-user')
	attrs = tooltip(attrs, name)
	printElement("fileCSS: " + str(attrs))
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