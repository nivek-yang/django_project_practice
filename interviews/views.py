from django.shortcuts import render
from .models import Interview

# Create your views here.
def index(req):
    # 抓面試列表
    # 請 model 從資料庫調出資料
    # select * from innterviews
    interviews = Interview.objects.all()
    return render(req, "interviews/index.html", {"interviews": interviews})

def new(req):
    return render(req, "interviews/new.html")