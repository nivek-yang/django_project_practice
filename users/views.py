from django.shortcuts import render

# Create your views here.
def sign_up(req):
    return render(req, "users/sign_up.html")