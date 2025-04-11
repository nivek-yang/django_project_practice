from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(req):
    return HttpResponse("hello")

def about(req):
    return HttpResponse("關於我們")

def contact(req):
    return HttpResponse("聯絡我們")