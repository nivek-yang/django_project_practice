from django.shortcuts import render

# Create your views here.

def index(req):
    return render(req, "pages/index.html")

def about(req):
    return render(req, "pages/about.html")

def contact(req):
    return render(req, "pages/contact.html")