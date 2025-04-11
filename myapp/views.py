from django.shortcuts import render

# Create your views here.

def home(req):
    return render(req, "myapp/home.html")

def about(req):
    return render(req, "myapp/about.html")

def contact(req):
    return render(req, "myapp/contact.html")