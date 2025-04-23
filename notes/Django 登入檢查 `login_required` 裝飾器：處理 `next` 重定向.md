---
title: Django 登入檢查 `login_required` 裝飾器：處理 `next` 重定向
date: 2025-04-24
categories:
  - [技術筆記]
tags:
  - Python
  - Django
---

# 登入檢查：`login_required`

## 原理與機制
Django 提供了 `@login_required` 裝飾器，用於保護視圖，確保只有已登入的用戶才能訪問特定的頁面。當未登入的用戶嘗試訪問受保護的視圖時，Django 會自動將用戶重定向到設定中的 `LOGIN_URL`，並附加一個 `next` 查詢參數 (`QueryString`)，表示用戶原本想訪問的 URL。

## 使用範例
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def protected_view(req):
    return render(req, "protected_page.html")
```

## 工作原理
1. 當用戶訪問被 `@login_required` 裝飾的視圖時，Django 會檢查 `req.user.is_authenticated` 的值。
2. 如果 `req.user.is_authenticated` 為 `True`，則允許訪問該視圖。
3. 如果 `req.user.is_authenticated` 為 `False`，則會將用戶重定向到 `settings.LOGIN_URL`，並附加 `next` 查詢參數，指向用戶原本想訪問的 URL。

## 關鍵點
- **`req.user.is_authenticated`** 是一個屬性，用於判斷當前用戶是否已登入。
  - 如果用戶已登入，`req.user` 是一個 `User` 對象，且 `is_authenticated` 為 `True`。
  - 如果用戶未登入，`req.user` 是一個 `AnonymousUser` 對象，且 `is_authenticated` 為 `False`。

## 相關代碼（簡化版）
`@login_required` 的內部邏輯類似於以下代碼：
```python
from django.shortcuts import redirect
from django.conf import settings

def login_required(view_func):
    def wrapper(req, *args, **kwargs):
        if req.user.is_authenticated:
            return view_func(req, *args, **kwargs)
        else:
            login_url = settings.LOGIN_URL
            return redirect(f"{login_url}?next={req.path}")
    return wrapper
```

`@login_required` 的授權條件是基於 `req.user.is_authenticated` 的值。如果你需要自定義授權邏輯，可以考慮使用 Django 的 `PermissionRequiredMixin` 或自定義裝飾器。


## 工作流程
1. 用戶訪問受保護的視圖。
2. 如果未登入，Django 會將用戶重定向到 `LOGIN_URL`，例如：
   ```
   /users/sign_in?next=/protected_page
   ```
3. Django 不會自動處理 next 的重定向邏輯，需要在登入處理的視圖中手動處理 next 的值，並根據它進行重定向。

---

# 如何處理 `next`

## 原理與機制
`next` 是一個查詢參數，用於保存用戶在未登入時嘗試訪問的目標頁面。當用戶成功登入後，應該根據 `next` 的值將用戶重定向到該頁面。

### 1. **在登入表單中傳遞 `next`**
在登入頁面中，將 `next` 的值作為隱藏字段傳遞到表單中，這樣用戶提交表單時，`next` 的值會被一併提交。

sign_in.html
```html
<form action="{% url 'users:create_session' %}" method="post">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ next }}" />
    <input type="text" name="username" placeholder="Username" />
    <input type="password" name="password" placeholder="Password" />
    <button type="submit">登入</button>
</form>
```

---

### 2. **在後端處理 `next`**
在處理登入的視圖中，檢查 `req.POST` 或 `req.GET` 中是否有 `next` 的值，並在登入成功後進行重定向。

users/views.py
```python
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

def sign_in(req):
    next = req.GET.get("next", reverse("pages:index"))
    
    return render(req, "users/sign_in.html", {"next": next})

def create_session(req):
    username = req.POST['username']
    password = req.POST['password']

    user = authenticate(username=username, password=password)
    if user is not None:
        login(req, user)
        next = req.POST.get("next", reverse("pages:index"))

        return redirect(next)
    else:
        return redirect("users:sign_in")
```

## 工作流程
1. **未登入用戶訪問受保護頁面**  
   用戶被重定向到登入頁面，並附加 `next` 查詢參數，例如：
   ```
   /users/sign_in?next=/protected_page
   ```

2. **用戶提交登入表單**  
   表單中包含 `next` 的值，後端接收該值。

3. **後端處理重定向**  
   後端檢查 `next` 的值，並在登入成功後將用戶重定向到該頁面。如果 `next` 不存在，則重定向到預設頁面（如首頁）。

---

# QueryString

## 原理與機制
QueryString 是 URL 中的查詢參數部分，用於在 URL 中傳遞數據。格式如下：
```
/path/to/page?key1=value1&key2=value2
```
在 Django 中，可以使用 `req.GET` 獲取 QueryString 中的參數。

## 使用範例
```python
def example_view(req):
    value = req.GET.get('key', 'default_value')
    return render(req, "example.html", {"value": value})
```

## 工作流程
1. 用戶訪問包含 QueryString 的 URL，例如：
   ```
   /example?key=hello
   ```
2. Django 通過 `req.GET` 提供訪問 QueryString 的方法。

---

# 總結

- 使用 `@login_required` 確保視圖只能被已登入用戶訪問。
- 通過處理 `next` 查詢參數，實現用戶登入後的重定向。
- 利用 QueryString 傳遞數據，實現靈活的頁面交互。
- 使用 `logout` 方法實現安全的登出功能。
- 通過外鍵將 `Interview` 和 `Comment` 關聯到 `User`，實現數據的關聯性。

這些功能構成了 Django 中用戶認證與權限管理的基礎，為構建安全、可靠的應用提供了強大的支持。
