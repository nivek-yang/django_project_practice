from django.shortcuts import render

# Create your views here.
def home(req):
    return render(req, "myapp2/home.html")

def about(req):
    return render(req, "myapp2/about.html")

def contact(req):
    return render(req, "myapp2/contact.html")