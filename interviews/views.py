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

def show(req, id): # 參數要多加 id，從 urls 傳來的關鍵字引數
    # 抓資料
    # pk = primary key = 主鍵
    interview = Interview.objects.get(pk=id)
    return render(req, "interviews/show.html", {"interview": interview})