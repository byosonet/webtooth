from django.shortcuts import render, redirect
from webtooth.config import logger, updatePropertie, loadPropertie, getLogin
from webtooth.signals import getUser
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from webtooth.decorators import validRequest

import json

# Create your views here.
log = logger('appproperties', True)

@login_required(login_url=getLogin())
@validRequest
def updateClassMenu(request):
    try:
        if request.method == 'POST':
            log.debug("Method POST with params: "+str(request.POST))
            for p in request.POST:
                log.debug("field: {}, value: {}".format(p, request.POST.get(p)))
            if request.POST.get('classMenu') != None:
                updatePropertie(userRequest(), 'class_menu', request.POST.get('classMenu'))
                loadPropertie(userRequest(), request)
            data = json.dumps({'result': 'OK'})
            return HttpResponse(data, content_type='application/json')
    except:
        data = json.dumps({'result': 'KO'})
        return HttpResponse(data, content_type='application/json')

@login_required(login_url=getLogin())
@validRequest
def updateFontMenu(request,value):
    updatePropertie(userRequest(), 'font_italic', value)
    loadPropertie(userRequest(), request)
    return redirect('/')

def userRequest():
    user = getUser()
    return user.id