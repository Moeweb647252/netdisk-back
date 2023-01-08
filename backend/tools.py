from django.http.response import JsonResponse
from django.contrib.sessions.backends.base import SessionBase
from .models import *
from django.http.request import HttpRequest
import hashlib, time

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
 
  Returns:
    _type_: _description_
  """ 
  if not code in STATUS_CODE.keys():
    raise Exception("Status Code not found.")
  respBody = STATUS_CODE[code].copy()
  respBody["data"] = data
  return JsonResponse(respBody)

def getUserByRequest(request: HttpRequest):
  token = request.GET.get("token", None)
  if not token:
    raise BackendException(generateApiResponse(2202))
  user = User.objects.filter(token=token).first()
  if not user:
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

def getRequiredArgFromPostRequest(request: HttpRequest, **args):
  res = []
  for i in args:
    tmp = request.GET.get(i)
    if not i:
      raise BackendException(generateApiResponse(2000))
    res.append(tmp)
  return tuple(res)

def generateToken():
  return md5Encode(str(time.time()))