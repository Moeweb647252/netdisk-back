from django.shortcuts import render
from django.http.request import HttpRequest
from .models import *


# Create your views here.

def login(request: HttpRequest):
    un = request.POST.get()
