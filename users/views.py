from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
# django decorator
from django.views.decorators.http import require_POST
from django.urls import reverse

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

    # next: 之後要到哪個 url
    # 字典裡沒有 next 會出錯
    # next = req.GET['next']
    
    # 改用 get，沒有 next 不會出錯，用預設值會回到首頁
    # 用 reverse 讓使用者看不到首頁的 namespacing
    next = req.GET.get("next", reverse("pages:index"))
    
    return render(req, "users/sign_in.html", {"next": next})

@require_POST
def create_session(req):
    username = req.POST['username']
    password = req.POST['password']

    user = authenticate(
        username=username,
        password=password)
    
    if user is not None:
        login(req, user) # cookie 給瀏覽器，session 存 server
        # @login_required 返回 LOGIN_URL 後會在網址後面加 QueryString ?next=<原本的 url>
        # 處理 next
        next = req.POST.get("next", reverse("pages:index"))

        return redirect(next)
    else:
        return redirect("users:sign_in")

@require_POST
def delete_session(req):
    logout(req)

    return redirect("pages:index")
