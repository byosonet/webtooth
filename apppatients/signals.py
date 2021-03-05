from apppatients.middleware import RequestMiddleware
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.signals import request_finished
from django.contrib.admin.models import LogEntry
from django.utils import timezone
from django.contrib.auth.models import User
from apppatients.models import Navigation
import logging
import json

log = logging.getLogger('apppatients.signals')

@receiver(post_save)
def auditAddUpdateLog(sender, instance, created, raw, update_fields, **kwargs):
  
  list_of_models = ['Patient','Adress','File',]
  
  if sender.__name__ not in list_of_models:
    return
  
  user = getUser()
  path = getRequestPath()
  if created:
    instance.saveAddition(user,path)
  elif not raw:
    instance.saveEdition(user,path)

@receiver(post_delete)
def auditDeleteLog(sender, instance, **kwargs):
  
  list_of_models = ['Patient','Adress','File',]

  if sender.__name__ not in list_of_models:
    return

  user = getUser() 
  path = getRequestPath()
  instance.saveDeletion(user,path)

@receiver(request_finished)
def captureRequest(sender, **kwargs):
  user = getUser()
  #path = getRequestPath()
  #insertLogEntryAmdin(user,path)
  request = getRequest()
  response = getResponse()
  insertModelNavigation(user,request,response)

def getUser():
  thread_local = RequestMiddleware.thread_local
  if hasattr(thread_local, 'user'):
    user = thread_local.user
  else:
    user = None
  return user

def getRequestPath():
  thread_local = RequestMiddleware.thread_local
  if hasattr(thread_local, 'path'):
    path = thread_local.path
  else:
    path = "None"
  return path

def getRequest():
  thread_local = RequestMiddleware.thread_local
  if hasattr(thread_local, 'request'):
    request = thread_local.request
  else:
    request = None
  return request

def getResponse():
  thread_local = RequestMiddleware.thread_local
  if hasattr(thread_local, 'response'):
    response = thread_local.response
  else:
    response = None
  return response

def insertLogEntryAmdin(user,path):
    message = 'url: {}, se ha consultado'.format(path)
    if user.id:
      LogEntry.objects.create(
        user_id         = user.id,
        content_type_id = 1,
        object_id       = 0,
        object_repr     = "path:"+str(path),
        action_flag     = 0,
        change_message = message
      )

def insertModelNavigation(user,req,res):
  userName=""
  userId=0
  if hasattr(user,'id') and user.id != None:
    if hasattr(user,'first_name') and user.first_name != '':
      userName = str(user.get_full_name())
      log.info("Username: "+userName)
    else:
      userName = str(user)
      log.info("Username: "+userName)
    userId = user.id
  else:
    userName = str(user)
    log.info("Username: "+userName)
  ###log.info("Userid: "+str(userId))

  userCode=""
  if user.get_username():
    userCode = str(user.get_username())
  else:
    userCode = userName
  ###log.info("Usercode: "+userCode)

  permissions = ""
  if user.get_all_permissions():
    superuser = User.objects.get(pk=user.id)
    if not superuser.is_superuser:
      permissions = str(user.get_all_permissions())
    else:
      permissions = "{Superuser}"
  else:
    permissions = "{}"
  log.info("Permissions: "+permissions)

  method=str(req.method)
  ###log.info("Request method: "+method)
  
  fullpath=str(req.get_full_path())
  log.info("Request: "+method+":"+fullpath)
  
  status = res.status_code
  ###log.info("Status: "+str(status))
  
  data=""
  if req.POST:
    data=str(json.dumps(req.POST))
  else:
    data="{}"
  log.debug("Data send: "+data)
  
  host = str(req.get_host())
  log.info("Host: "+host)
  
  nameF="ninguno"
  for filename, blob in req.FILES.items():
    nameF = str(req.FILES[filename].name)
    
  ###log.info("File received: "+nameF)

  varSession = str(json.dumps({'vars':list(req.session.keys())}))
  log.debug("Session var: "+varSession)

  try:
    headers = str(req.headers.get('User-Agent'))
    log.info("App/Origin: "+headers)
  except:
    pass

  updateDate = timezone.localtime(timezone.now())
  ###log.info("Event time: "+str(updateDate))

  Navigation.objects.create(
    userName=userName,
    userId=userId,
    userCode=userCode,
    permission=permissions,
    method=method,
    path=fullpath,
    status=status,
    data=data,
    host=host,
    file=nameF,
    varSession=varSession,
    eventTime=updateDate
  )
