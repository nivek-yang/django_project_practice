from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, "interviews/index.html")

def new(req):
    return render(req, "interviews/new.html")