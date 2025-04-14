from django.shortcuts import render

# Create your views here.
def home(req):
    return render(req, "interviews/home.html")

def new(req):
    return render(req, "interviews/new.html")