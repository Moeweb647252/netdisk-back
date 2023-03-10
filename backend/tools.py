from django.http.response import JsonResponse
from .models import *
from django.http.request import HttpRequest
import hashlib, time
import json

class BackendException(Exception):
  pass

STATUS_CODE = {
  1000: {"code": 1000}, 
  2000: {"code": 2000}, 
  2001: {"code": 2001}, 
  2101: {"code": 2101}, 
  2201: {"code": 2201},
  2202: {"code": 2202},
  2203: {"code": 2203},
  2301: {"code": 2301}
}

def md5Encode(str:str):
  md5 = hashlib.md5()
  md5.update(str.encode())
  return md5.hexdigest()

def generateApiResponse(code:int=100,data:object=None):
  """_summary_

  Args:
    code (int, optional): _description_. Defaults to 100.
    data (object, optional): _description_. Defaults to None.
  
  Code:
    1000: Success.
    2000: Error.
    2001: Error: Missing parameter.
    2101: FileSystem Error: File or Directory not found.
    2201: Access Error: Permission Denied
    2202: Access Error: Not logged in
    2203: Access Error: Incorrect user credentials
    2301: InternalError
    2401: Configure Error: Configuration Not found
 
  Returns:
    _type_: _description_
  """ 
  if not code in STATUS_CODE.keys():
    raise Exception("Status Code not found.")
  respBody = STATUS_CODE[code].copy()
  respBody["data"] = data
  return JsonResponse(respBody)

def getUserOrNoneByRequest(request: HttpRequest):
  token = request.GET.get("token", None)
  if token is None:
    token = request.POST.get("token", None)
  if token is None:
    token = json.loads(request.body).get("token")
  if token is None:
    return None
  user = User.objects.filter(token=token).first()
  if user is None:
    return None
  return user

def getUserByRequest(request: HttpRequest):
  user = getUserOrNoneByRequest(request)
  if user is None:
    raise BackendException(generateApiResponse(2201))
  return user

def getRequiredArgFromGetRequest(request: HttpRequest, *args):
  res = []
  for i in args:
    tmp = request.GET.get(i)
    if not tmp:
      raise BackendException(generateApiResponse(2000))
    res.append(tmp)
  return tuple(res)

def getRequiredArgFromPostRequest(request: HttpRequest, *args):
  res = []
  for i in args:
    tmp = request.POST.get(i)
    if not tmp:
      raise BackendException(generateApiResponse(2000))
    res.append(tmp)
  return tuple(res)

def getRequiredArgFromJsonRequest(request: HttpRequest, *args):
  res = []
  req:dict = json.loads(request.body)
  for i in args:
    tmp = req.get(i)
    print(i, tmp)
    if tmp is None:
      raise BackendException(generateApiResponse(2000))
    res.append(tmp)
  return tuple(res)

def generateToken():
  return md5Encode(str(time.time()))

def checkFsPermission(fs: FileSystem, user:User, operate:int):
  fs_permissions = [int(i) for i in fs.permissions]
  permission = fs_permissions[0]
  if not user is None:
    if len(fs.owner_users.filter(id=user.id)):
      permission = max(permission, fs_permissions[2])
    for group in fs.owner_groups:
        if len(user.group_set.filter(id=group.id)):
          if fs_permissions[1] > permission:
            permission = max(permission, fs_permissions[1])
  if permission == operate:
    return True
  if permission == 6:
    return True
  return False

def checkFsPermissionExp(*args, **kwargs):
  if checkFsPermission(*args, **kwargs):
    return True
  raise BackendException(generateApiResponse(2201))

def getFsById(fs_id):
  fs = FileSystem.objects.filter(id=fs_id).first()
  if fs is None:
    raise BackendException(generateApiResponse(2301))
  fs:FileSystem = fs.first()
  return fs

def getSettingsItem(name):
  item = Settings.objects.filter(name=name).first()
  if item is None:
    raise BackendException(generateApiResponse(2401))
  return item

def createGroupFs(group:Group, name:str, device_id:int=None):
  if device_id is None:
    device_id = getSettingsItem("DefaultDevice").value
  fs = FileSystem(
    name=name,
    owner_groups=[group],
    owner_users=[i for i in group.admins],
    permissions="",
  )
  fs.save()
  return fs