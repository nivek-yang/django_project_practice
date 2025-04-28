from django.shortcuts import render, get_object_or_404, redirect
from .models import Interview, Comment, FavoriteInterview
from django.http import HttpResponse, Http404
from django.urls import reverse
from .forms import InterviewForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

# Create your views here.
def index(req):

    # 新增資料
    if req.POST:
        form = InterviewForm(req.POST) # 用 form 解決寫入資料庫麻煩的過程，沒有加 instance 參數代表想增加資料
        
        # interview = form.save() # 成功儲存後回傳該 instance

        # 加入 user 欄位
        interview = form.save(commit=False) # 先把資料準備好，不存到資料庫
        interview.user = req.user
        interview.save()
        
        # --------------------------------------
        # DEPRECATED: 舊的實作方式
        # 原因: 效能較差，程式碼冗長
        # 替代方案: 使用 InterviewForm
        
        # 處理表單提交：新增面試記錄
        # 從 POST 請求中獲取表單數據
        # company_name = req.POST['company_name']
        # position = req.POST['position']
        # interview_date = req.POST['interview_date']
        # rating = req.POST['rating']
        # review = req.POST['review']
        # result = req.POST['result']

        # 在資料庫中創建新的面試記錄
        # interview = Interview.objects.create(
        #     company_name=company_name,
        #     position=position,
        #     interview_date=interview_date,
        #     rating=rating,
        #     review=review,
        #     result=result,
        # )
        # --------------------------------------
        
        return redirect("interviews:show", id=interview.id)
    else:
        # 顯示所有面試記錄列表
        # 從資料庫中獲取所有面試記錄
        interviews = Interview.objects.order_by("-id") # 依 id 反向排序
        return render(req, "interviews/index.html", {"interviews": interviews})

# 檢查是否有登入
# @login_required(login_url="users:sign_in")
@login_required
def new(req):
    form = InterviewForm
    return render(req, "interviews/new.html", {"form": form})

@login_required
def show(req, id): # 參數要多加 id，從 urls 傳來的關鍵字引數
    interview = get_object_or_404(Interview, pk=id)

    # 更新資料，因為 HTML 只支援 GET, POST 兩種方法，用 POST 來達到 PUT/PATCH 的效果
    if req.POST:
        form = InterviewForm(req.POST, instance=interview) # 有加 instance 參數代表想更新資料
        form.save()

        # --------------------------------------
        # DEPRECATED: 舊的實作方式
        # 原因: 效能較差，程式碼冗長
        # 替代方案: 使用 InterviewForm
        
        # company_name = req.POST['company_name']
        # position = req.POST['position']
        # interview_date = req.POST['interview_date']
        # rating = req.POST['rating']
        # review = req.POST['review']
        # result = req.POST['result']
        
        # interview.company_name = company_name
        # interview.position = position
        # interview.interview_date = interview_date
        # interview.rating = rating
        # interview.review = review
        # interview.result = result

        # 更新
        # interview.save()

        # --------------------------------------

        return redirect("interviews:show", interview.id)

    else:
        # 抓資料
        # pk = primary key = 主鍵

        # --------------------------------------
        # DEPRECATED: 舊的實作方式
        # 用 get_object_or_404 替代 (已移到 if 條件之外)
        # try:
        #   interview = Interview.objects.get(pk=id)
        # except:
        #   raise Http404("Interview does not exist")
        # --------------------------------------
        
        # --------------------------------------
        # DEPRECATED: Comment 角度抓取 interview 的所有留言
        # 改用 Interview 角度

        # comments = Comment.objects.filter(interview=interview)
        # --------------------------------------
        
        # Interview 角度
        comments = interview.comment_set.all()
        return render(req, "interviews/show.html", {"interview": interview, "comments": comments})

@login_required
def edit(req, id): # 參數要多加 id，從 urls 傳來的關鍵字引數
    interview = get_object_or_404(Interview, pk=id)
    form = InterviewForm(instance=interview)
    
    return render(req, "interviews/edit.html", {"interview": interview, "form": form})

@login_required
def delete(req, id):
    interview = get_object_or_404(Interview, pk=id)
    # soft delete
    # interview.is_delete = True
    # interview.save()
    
    # hard delete
    interview.delete()

    return redirect("interviews:index")

@require_POST
@login_required
def comment(req, id):
    interview = get_object_or_404(Interview, pk=id)
    # 建立留言

    # Interview 角度
    # 1 : N
    # interview has many comments
    # interview.comment_set
    # comment_set 是虛擬的東西，不是真正的欄位，而是 QuerySet
    # 拿 interview 資料的所有留言，讓新增的時候不用寫 id，較方便
    interview.comment_set.create(
        content = req.POST['content'],
        user=req.user
        )
    
    # Comment 角度
    # --------------------------------------
    # DEPRECATED: 
    # 改用 Interview 角度

    # Comment.objects.create(content = req.POST['content'],
    #                       # interview_id = id,
    #                       interview=interview,
    #                       )
    # --------------------------------------
    
    # redirect
    return redirect("interviews:show", id=interview.id)

@require_POST
@login_required
def favorite(req, id):
    interview = get_object_or_404(Interview, pk=id)
    user = req.user

    # # 判斷這位使用者是否已經按過讚
    # if user.favorite_interviews.filter(pk=interview.pk).exists():
    #     # 如果有按過讚，則取消按讚（remove）
    #     user.favorite_interviews.remove(interview)
    # else:
    #     # 如果沒有按過讚，則加上（add）
    #     user.favorite_interviews.add(interview)

    # 從 FavoriteInterview model 的角度
    favorite_interview = FavoriteInterview.objects.filter(user=user, interview=interview)

    if favorite_interview.exists():
        favorite_interview.delete()
    else:
        FavoriteInterview.objects.create(user=user, interview=interview)

    return redirect("interviews:show", id=interview.id)


    
    
