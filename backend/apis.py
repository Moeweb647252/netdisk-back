from django.http.response import JsonResponse
from django.http.request import HttpRequest
from .tools import *
from .models import *
from .storage import globalStorage
from .urls import routeApi
import os
import json
import shutil

@routeApi("user/login")
def userLogin(request:HttpRequest):
  try:
    name,password = getRequiredArgFromGetRequest(request, "name", "password")
  except BackendException as e:
    return e.args[0]
  user = User.objects.filter(name=name).first()
  if not user:
    return generateApiResponse(2203)
  if password != md5Encode(user.password):
    return generateApiResponse(2203)
  return generateApiResponse(1000, {
    "name": user.name,
    "token": user.token,
    
  })
  
  
@routeApi("fs/files")
def fsUserGetFiles(request:HttpRequest):
  try:
    user = getUserByRequest(request)
  except BackendException as e:
    return e.args[0]
  try:
    path, fsId = getRequiredArgFromGetRequest(request, "path", "fsId")
  except BackendException as e:
    return e.args[0]
  path = request.GET.get("path", "")
  realPath = os.path.join(user.path, path)
  if not os.path.isdir(realPath):
    return generateApiResponse(2101)
  res = [
    {
      "name": i,
      "isDir": os.path.isdir(os.path.join(realPath,i)),
      "stat":os.stat(os.path.join(realPath,i)),
      "path": os.path.join(path, i)
    }
    for i in filter(
      lambda obj:not obj.startswith("."),
      os.listdir(realPath)
    )
  ]
  return generateApiResponse(1000, res)

@routeApi("fs/paste")
def fsAllPasteFile(request:HttpRequest):
  try:
    fsType,pasteFiles,destPath,removeSource = getRequiredArgFromJsonRequest(request, "fsType", "pasteFiles", "destPath", "removeSource")
  except BackendException as e:
    return e.args[0]
  if fsType == "user":
    user = getUserByRequest(request)
    originPath = user.path
    realDestPath = os.path.join(originPath,destPath)
  if not os.path.exists(realDestPath):
    return generateApiResponse(2101)
  if not os.access(realDestPath, os.R_OK):
    return generateApiResponse(2201)
  for i in pasteFiles:
    realPath = os.path.join(originPath,i)
    if not os.path.exists(realPath):
      return generateApiResponse(2101)
    if not os.access(realPath, os.R_OK):
      return generateApiResponse(2201)
    if removeSource == "True":
      if not os.access(realPath, os.W_OK):
        return generateApiResponse(2201)
      os.rename(realPath, os.path.join(realDestPath,os.path.split(realPath)[-1]))
    else:
      if os.path.isdir(realPath):
        shutil.copytree(realPath, os.path.join(realDestPath,os.path.split(realPath)[-1]))
      else:
        shutil.copy(realPath, os.path.join(realDestPath,os.path.split(realPath)[-1]))
  return generateApiResponse(1000)

def userGetInfo(request:HttpRequest):
  pass

def userSetInfo(request:HttpRequest):
  pass
