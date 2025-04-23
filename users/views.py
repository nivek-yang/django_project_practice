from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# django decorator
from django.views.decorators.http import require_POST

# Create your views here.
@require_POST
def index(req):
    form = UserCreationForm(req.POST)
    if form.is_valid():
        form.save()

    return redirect("pages:index")
    

def sign_up(req):
    form = UserCreationForm
    return render(req, "users/sign_up.html", {"form": form})

def sign_in(req):
    # cookie 瀏覽器 號碼牌，設有效期限
    # session 伺服器
    return render(req, "users/sign_in.html")

@require_POST
def create_session(req):
    username = req.POST['username']
    password = req.POST['password']

    user = authenticate(
        username=username,
        password=password)
    
    if user is not None:
        login(req, user) # cookie 給瀏覽器，session 存 server

        return redirect("pages:index")
    else:
        return redirect("users:sign_in")

@require_POST
def delete_session(req):
    logout(req)

    return redirect("pages:index")
