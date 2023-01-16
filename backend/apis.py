from django.http.response import JsonResponse
from django.http.request import HttpRequest
from .tools import *
from .models import *
from .storage import *
from .urls import routeApi
import os
import json
import shutil  
  
@routeApi("fs/files")
def fsUserGetFiles(request:HttpRequest):
  user = getUserOrNoneByRequest(request)
  path, fs_id = getRequiredArgFromGetRequest(request, "path", "fs_id")
  fs = getFsById(fs_id)
  checkFsPermissionExp(fs, user, 2) # check permission for read operation
  real_path = os.path.join(fs.path, path)
  if not os.path.isdir(real_path):
    return generateApiResponse(2101)
  res = [
    {
      "name": i,
      "isDir": os.path.isdir(os.path.join(real_path,i)),
      "stat":os.stat(os.path.join(real_path,i)),
      "path": os.path.join(path, i)
    }
    for i in filter(
      lambda obj:not obj.startswith("."),
      os.listdir(real_path)
    )
  ]
  return generateApiResponse(1000, res)

@routeApi("fs/paste")
def fsAllPasteFile(request:HttpRequest):
  fs_id,paste_files,remove_source = getRequiredArgFromJsonRequest(request, "fs_id", "paste_files", "dest_path", "remove_source")
  fs = getFsById(fs_id)
  user = getUserOrNoneByRequest(request)
  checkFsPermissionExp(fs, user, 6) # check permission for read and write
  origin_path = fs.path
  for i in paste_files:
    real_path = os.path.join(origin_path,i[0])
    real_dest_path = os.path.join(origin_path,i[1])
    if not os.path.exists(real_dest_path):
      return generateApiResponse(2101)
    if not os.access(real_dest_path, os.R_OK):
      return generateApiResponse(2201)
    if not os.path.exists(real_path):
      return generateApiResponse(2101)
    if not os.access(real_path, os.R_OK):
      return generateApiResponse(2201)
    if remove_source == "True":
      if not os.access(real_path, os.W_OK):
        return generateApiResponse(2201)
      os.rename(real_path, os.path.join(real_dest_path,os.path.split(real_path)[-1]))
    else:
      if os.path.isdir(real_path):
        shutil.copytree(real_path, os.path.join(real_dest_path,os.path.split(real_path)[-1]))
      else:
        shutil.copy(real_path, os.path.join(real_dest_path,os.path.split(real_path)[-1]))
  return generateApiResponse(1000)

@routeApi("fs/downloadToken")
def fsGetDownloadToken(request:HttpRequest):
  user = getUserOrNoneByRequest(request)
  fs_id, path = getRequiredArgFromGetRequest("fs_id", "path")
  fs = getFsById(fs_id)
  checkFsPermissionExp(fs, user, 2)
  token = generateToken()
  globalStorage.downloadLinks[token] = DownloadLink(int(time.time) + 86400, token, os.path.join(fs.path, path))
  return generateApiResponse(1000, {"token": token})

@routeApi("user/getSelfInfo")
def userGetSelfInfo(request:HttpRequest):
  user = getUserByRequest(request)
  return generateApiResponse(1000, {
    "name": user.name,
    "fs_id": user.fs.id,
    "permissionLevel": user.permission_level,
    "email": user.email
  })

@routeApi("user/setSelfInfo")
def userSetSelfInfo(request:HttpRequest):
  pass

@routeApi("user/login")
def userLogin(request:HttpRequest):
  name,password = getRequiredArgFromPostRequest(request, "name", "password")
  user = User.objects.filter(name=name).first()
  if user is None:
    return generateApiResponse(2203)
  if password != md5Encode(user.password):
      return generateApiResponse(2203)
  return generateApiResponse(1000, {
    "name": user.name,
    "fs_id": user.fs.id,
    "permissionLevel": user.permission_level,
    "email": user.email
  })

@routeApi("group/create")
def groupCreate(request:HttpRequest):
  name = getRequiredArgFromPostRequest(request, "name")
  user = getUserByRequest(request)
  group = Group(name=name)
  group.save()
  group.admins.add(user)
  group.users.add(user)
  group.save()
  createGroupFs(group, group.name)
  return generateApiResponse(1000)

@routeApi("group/addUser")
def groupAddUser(request:HttpRequest):
  user_id, group_id = getRequiredArgFromGetRequest(request, "user_id", "group_id")  
  user = getUserByRequest(request)
  #check if user one of the group's admin
  group = Group.objects.filter(id=group_id).first()
  if group is None:
    return generateApiResponse(2301)
  target_user = User.objects.filter(id=user_id).first()
  if target_user is None:
    return generateApiResponse(2301)
  if not user in group.admins.all():
    return generateApiResponse(2201)
  group.users.add(target_user)
  return generateApiResponse(1000)

@routeApi("group/removeUser")
def groupRemoveUser(request:HttpRequest):
  user_id, group_id = getRequiredArgFromGetRequest(request, "user_id", "group_id")
  user = getUserByRequest(request)
  #check if user one of the group's admin
  group = Group.objects.filter(id=group_id).first()
  if group is None:
    return generateApiResponse(2301)
  target_user = User.objects.filter(id=user_id).first()
  if target_user is None:
    return generateApiResponse(2301)
  if not user in group.admins.all():
    return generateApiResponse(2201)
  if target_user in group.users.all():
    return generateApiResponse(2301)
  return generateApiResponse(1000)
