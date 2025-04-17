# Django 面試記錄系統 - CRUD 操作筆記

## 1. Create (新增)
```python
# views.py
def index(req):
    if req.POST:
        # 處理表單提交：新增面試記錄
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
        
        # 新增成功後重定向到詳細頁面 "<int:id>/"，所以要設定 id 參數
        return redirect("interviews:show", id=interview.id)
```

## 2. Update (更新)
```python
# views.py
def edit(req, id):
    # 獲取要編輯的面試記錄
    interview = get_object_or_404(Interview, pk=id)
    
    if req.method == "POST":
        # 處理表單提交：更新面試記錄
        interview.company_name = req.POST['company_name']
        interview.position = req.POST['position']
        interview.interview_date = req.POST['interview_date']
        interview.rating = req.POST['rating']
        interview.review = req.POST['review']
        interview.result = req.POST['result']
        interview.save()
        
        # 更新成功後重定向到詳細頁面
        return redirect("interviews:show", id=interview.id)
    else:
        # 顯示編輯表單
        return render(req, "interviews/edit.html", {"interview": interview})
```

## 3. Delete (刪除)
```python
# views.py
def delete(req, id):
    # 獲取要刪除的面試記錄
    interview = get_object_or_404(Interview, pk=id)
    # 刪除記錄
    interview.delete()
    # 重定向到列表頁面
    return redirect("interviews:index")
```

## 4. 模板相關更新

### 詳細頁面 (show.html)
```html
<h1>公司: {{ interview.company_name }}</h1>
<h2>職位: {{ interview.position }}</h2>
<h2>面試日期: {{ interview.interview_date }}</h2>
<h3>評分: {{ interview.rating }}/10</h3>
<p>心得: {{ interview.review }}</p>

<!-- 導航連結 -->
<a href="{% url "interviews:index" %}">回上一頁</a>
<a href="{% url "interviews:edit" interview.id %}">編輯</a>

<!-- 刪除表單 -->
<form action="{% url "interviews:delete" interview.id %}" method="post" onsubmit="return confirm('是否確認刪除？')">
    {% csrf_token %}
    <button>刪除</button>
</form>
```

## 5. URL 配置
```python
# urls.py
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("<int:id>", views.show, name="show"),
    path("<int:id>/edit", views.edit, name="edit"),
    path("<int:id>/delete", views.delete, name="delete")
]
```

## 6. 重要注意事項

1. **CSRF 保護**
   - 所有 POST 請求的表單都需要包含 `{% csrf_token %}`
   - 這是 Django 的安全機制，防止跨站請求偽造

2. **URL 命名空間**
   - 使用 `interviews:edit` 而不是 `interviews.edit`
   - 冒號 `:` 是 Django URL 命名空間的正確語法

3. **刪除確認**
   - 使用 `onsubmit="return confirm('是否確認刪除？')"` 添加刪除確認對話框
   - 使用單引號避免與外層雙引號衝突

4. **重定向**
   - 新增後重定向到詳細頁面
   - 更新後重定向到詳細頁面
   - 刪除後重定向到列表頁面 

5. **錯誤處理**
   - 使用 `get_object_or_404` 處理不存在的記錄
   - 避免直接使用 `get()` 方法，因為它會拋出 `DoesNotExist` 異常
   - 在表單處理時要考慮數據驗證

6. **請求方法判斷**
   - 使用 `req.method == "POST"` 判斷是否為表單提交
   - GET 請求用於顯示頁面
   - POST 請求用於處理表單數據

7. **模板繼承**
   - 使用 `{% extends "base.html" %}` 繼承基礎模板
   - 使用 `{% block content %}` 定義可替換的內容區塊
   - 保持模板結構的一致性

8. **數據庫操作**
   - 使用 `objects.create()` 創建新記錄
   - 使用 `save()` 更新現有記錄
   - 使用 `delete()` 刪除記錄
   - 注意事務處理，確保數據一致性

9. **安全性考慮**
   - 所有用戶輸入都需要驗證
   - 使用 Django 的表單類進行數據驗證
   - 避免直接使用用戶輸入構建查詢
   - 注意 SQL 注入防護

10. **性能優化**
    - 使用 `select_related()` 或 `prefetch_related()` 優化關聯查詢
    - 避免 N+1 查詢問題
    - 考慮使用緩存提高性能

11. **代碼組織**
    - 遵循 Django 的 MTV 模式
    - 保持視圖函數簡潔
    - 將業務邏輯放在模型或服務層
    - 使用類視圖（Class-based Views）簡化代碼 