from django.shortcuts import render
from .forms import UserForm

# Create your views here.
def sign_up(req):
    form = UserForm
    return render(req, "users/sign_up.html", {"form": form})