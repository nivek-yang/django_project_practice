# Django Model 的 QuerySet 說明

## 1. 基本概念
QuerySet 是 Django 中資料庫查詢的主要介面，它代表了一個資料庫查詢的集合。

## 2. 常用 QuerySet 方法

### 2.1 基本查詢
```python
# 獲取所有記錄
Interview.objects.all()

# 獲取單一記錄
Interview.objects.get(pk=1)  # 主鍵查詢
Interview.objects.get(company_name="某公司")  # 欄位查詢

# 過濾記錄
Interview.objects.filter(company_name="某公司")  # 等於
Interview.objects.exclude(company_name="某公司")  # 不等於
```

### 2.2 鏈式查詢
```python
# 可以連續使用多個方法
Interview.objects.filter(
    company_name="某公司"
).exclude(
    result="未錄取"
).order_by("-interview_date")
```

### 2.3 排序
```python
# 升序排序
Interview.objects.order_by("interview_date")

# 降序排序
Interview.objects.order_by("-interview_date")

# 多欄位排序
Interview.objects.order_by("company_name", "-interview_date")
```

### 2.4 限制查詢結果
```python
# 獲取前 5 條記錄
Interview.objects.all()[:5]

# 獲取第 6-10 條記錄
Interview.objects.all()[5:10]

# 獲取第一條記錄
Interview.objects.first()

# 獲取最後一條記錄
Interview.objects.last()
```

### 2.5 聚合查詢
```python
from django.db.models import Avg, Count, Max, Min, Sum

# 計算平均值
Interview.objects.aggregate(Avg('rating'))

# 計算總數
Interview.objects.count()

# 分組統計
Interview.objects.values('company_name').annotate(count=Count('id'))
```

## 3. QuerySet 的特性

### 3.1 延遲執行 (Lazy Evaluation)
```python
# 此時不會執行資料庫查詢
queryset = Interview.objects.all()

# 只有在實際需要數據時才會執行查詢
for interview in queryset:
    print(interview.company_name)
```

### 3.2 快取 (Caching)
```python
# 第一次遍歷會執行查詢
for interview in queryset:
    print(interview.company_name)

# 第二次遍歷會使用快取的結果
for interview in queryset:
    print(interview.position)
```

## 4. 進階查詢

### 4.1 關聯查詢
```python
# 使用 select_related 優化一對一或一對多關係
Interview.objects.select_related('related_model')

# 使用 prefetch_related 優化多對多關係
Interview.objects.prefetch_related('many_to_many_field')
```

### 4.2 條件查詢
```python
# 大於
Interview.objects.filter(rating__gt=5)

# 小於
Interview.objects.filter(rating__lt=5)

# 包含
Interview.objects.filter(company_name__contains="科技")

# 開頭是
Interview.objects.filter(company_name__startswith="A")

# 結尾是
Interview.objects.filter(company_name__endswith="公司")
```

### 4.3 日期查詢
```python
from datetime import date, timedelta

# 今天的面試
Interview.objects.filter(interview_date=date.today())

# 最近 7 天的面試
Interview.objects.filter(
    interview_date__gte=date.today() - timedelta(days=7)
)
```

## 5. 效能優化

### 5.1 避免 N+1 查詢問題
```python
# 不好的寫法（會產生 N+1 查詢）
for interview in Interview.objects.all():
    print(interview.related_model.name)  # 每次循環都會查詢資料庫

# 好的寫法（使用 select_related）
for interview in Interview.objects.select_related('related_model').all():
    print(interview.related_model.name)  # 只會查詢一次資料庫
```

### 5.2 只選擇需要的欄位
```python
# 只獲取需要的欄位
Interview.objects.values('company_name', 'position')

# 使用 only() 指定要載入的欄位
Interview.objects.only('company_name', 'position')
```

## 6. 實際應用範例

### 6.1 統計面試結果
```python
# 統計各公司的面試結果
results = Interview.objects.values('company_name').annotate(
    total=Count('id'),
    passed=Count('id', filter=models.Q(result='錄取')),
    failed=Count('id', filter=models.Q(result='未錄取'))
)
```

### 6.2 查詢最近的面試
```python
# 獲取最近 30 天的面試，按公司分組
recent_interviews = Interview.objects.filter(
    interview_date__gte=date.today() - timedelta(days=30)
).values('company_name').annotate(
    count=Count('id'),
    avg_rating=Avg('rating')
).order_by('-count')
```

QuerySet 是 Django ORM 的核心功能，掌握這些方法可以讓你更有效率地操作資料庫。
