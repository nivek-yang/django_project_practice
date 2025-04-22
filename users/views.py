from django.shortcuts import render, redirect
from .forms import UserForm

# Create your views here.
def index(req):
    if req.method == "POST":
        form = UserForm(req.POST)
        if form.is_valid():
            form.save()

        return redirect("pages:index")
    

def sign_up(req):
    form = UserForm
    return render(req, "users/sign_up.html", {"form": form})