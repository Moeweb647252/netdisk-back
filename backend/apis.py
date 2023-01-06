from django.http.response import JsonResponse
from django.http.request import HttpRequest
from .tools import generateApiResponse
import os,time

def fileDirGetFiles(request:HttpRequest):
  stime = time.time()
  path = request.GET.get("path")
  if not path:
    return generateApiResponse(2001)
  
  if not os.path.isdir(path):
    return generateApiResponse(2101)
  res = [{"name": i, "isDir": os.path.isdir(os.path.join(path,i)), "stat":os.stat(os.path.join(path,i)), "path":path}  for i in filter(lambda obj:not obj.startswith(".") ,os.listdir(path))]
  print(time.time() - stime)
  return generateApiResponse(1000, res)
  