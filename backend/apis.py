from django.http.response import JsonResponse
from django.http.request import HttpRequest
from .tools import *
from .models import *
from .storage import globalStorage
from .urls import routeApi
import os,time
import hashlib

@routeApi("user/login")
def userLogin(request:HttpRequest):
  try:
    name,password = getRequiredArgFromGetRequest(request, "name", "password")
  except BackendException as e:
    return e.args[0]
  user = User.objects.filter(name=name).first()
  if not user:
    return generateApiResponse(2203)
  if password != hashlib.md5(user.password):
    return generateApiResponse(2203)
  return generateApiResponse(1000, {
    "name": user.name,
    "token": user.token,
    
  })
  
  
@routeApi("fs/user/files")
def fsUserGetFiles(request:HttpRequest):
  try:
    user = getUserByRequest(request)
  except BackendException as e:
    return e.args[0]
  path = request.GET.get("path")
  if not path:
    return generateApiResponse(2001)
  realPath = os.path.join(user.path, path)
  if not os.path.isdir(realPath):
    return generateApiResponse(2101)
  res = [
    {
      "name": i,
      "isDir": os.path.isdir(os.path.join(realPath,i)),
      "stat":os.stat(os.path.join(realPath,i)),
      "path":path
    }
    for i in filter(
      lambda obj:not obj.startswith("."),
      os.listdir(realPath)
    )
  ]
  return generateApiResponse(1000, res)

def userGetInfo(request:HttpRequest):
  pass

def userSetInfo(request:HttpRequest):
  pass

def fsGetDownloadLink(path, request:HttpRequest):
  pass
