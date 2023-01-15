from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse, StreamingHttpResponse
from .models import *
from .urls import *
from .storage import *
from .tools import *
import os
import mimetypes
from wsgiref.util import FileWrapper

# Create your views here.
@route("download/<str:token>")
def download(request:HttpRequest, token:str):
  if not token in globalStorage.downloadLinks.keys():
    return HttpResponse(403)
  path = globalStorage.downloadLinks[token]
  if not os.access(path, os.O_RDONLY):
    globalStorage.downloadLinks.pop(token)
    return HttpResponse(403)
  filename = os.path.basename(path)
  chunk_size = 8192
  response = StreamingHttpResponse(
      FileWrapper(
          open(path, "rb"),
          chunk_size,
      ),
      content_type=mimetypes.guess_type(path)[0],
  )
  response["Content-Length"] = os.path.getsize(path)
  response["Content-Disposition"] = f"attachment; filename={filename}"
  return response