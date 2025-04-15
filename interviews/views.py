from django.shortcuts import render, get_object_or_404, redirect
from .models import Interview
from django.http import HttpResponse, Http404
from django.urls import reverse

# Create your views here.
def index(req):
    if req.POST:
        # 處理表單提交：新增面試記錄
        # 從 POST 請求中獲取表單數據
        company_name = req.POST['company_name']
        position = req.POST['position']
        interview_date = req.POST['interview_date']
        rating = req.POST['rating']
        review = req.POST['review']
        result = req.POST['result']

        # 在資料庫中創建新的面試記錄
        interview = Interview.objects.create(
            company_name=company_name,
            position=position,
            interview_date=interview_date,
            rating=rating,
            review=review,
            result=result,
        )
        
        return redirect("interviews:show", id=interview.id)
    else:
        # 顯示所有面試記錄列表
        # 從資料庫中獲取所有面試記錄
        interviews = Interview.objects.order_by("-id") # 依 id 反向排序
        return render(req, "interviews/index.html", {"interviews": interviews})

def new(req):
    return render(req, "interviews/new.html")

def show(req, id): # 參數要多加 id，從 urls 傳來的關鍵字引數
    # 抓資料
    # pk = primary key = 主鍵
    # try:
    #     interview = Interview.objects.get(pk=id)
    # except:
    #     raise Http404("Interview does not exist")
    interview = get_object_or_404(Interview, pk=id)
    return render(req, "interviews/show.html", {"interview": interview})