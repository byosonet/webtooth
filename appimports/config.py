from webtooth.config import logger
log = logger('appimports.config', False)

def validErrors(form):
	for field in form.errors:
		form[field].field.widget.attrs['class'] += ' border-bottom-danger'

def addClass(attrs,cclass):
	attrs.update({'class':cclass})
	return attrs

def xlsCSS(name):
	attrs = {'accept': 'application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
	attrs = addClass(attrs, 'btn btn-secondary btn-user')
	attrs = tooltip(attrs, name)
	printElement("xlsCSS: " + str(attrs))
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