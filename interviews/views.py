from django.shortcuts import render, get_object_or_404
from .models import Interview
from django.http import HttpResponse, Http404

# Create your views here.
def index(req):
    if req.POST:
        # 新增
        company_name = req.POST['company_name']
        position = req.POST['position']
        interview_date = req.POST['interview_date']
        rating = req.POST['rating']
        review = req.POST['review']
        result = req.POST['result']

        interview = Interview.objects.create(
            company_name=company_name,
            position=position,
            interview_date=interview_date,
            rating=rating,
            review=review,
            result=result,
        )
        
        return HttpResponse("新增")
    else:
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
    interview = get_object_or_404(Interview, pk=id)
    # try:
    #     interview = Interview.objects.get(pk=id)
    # except:
    #     raise Http404("Interview does not exist")
    return render(req, "interviews/show.html", {"interview": interview})