---
title: Django `login()` 函數的運作機制
date: 2025-04-23
categories:
  - [技術筆記]
tags:
  - Python
  - Django
---

Django 提供的 `login()` 函數是用來處理用戶認證並建立會話 (session) 和 cookie 的核心工具。以下是該函數的完整流程及其背後的運作機制。

---

# 1. **`login()` 函數的作用**
`django.contrib.auth.login(request, user)` 是用來將已經通過身份驗證的用戶標記為「已登入」的函數。它會執行以下操作：
- 將用戶的 ID 存儲到 session 中。
- 更新 session 的相關數據。
- 設置用戶的身份驗證狀態，讓 `request.user` 可以用來驗證用戶。

---

# 2. **流程詳解**

## **(1) 用戶身份驗證**
在調用 `login()` 函數之前，通常需要先驗證用戶的身份，例如使用 `authenticate()` 函數：

```python
from django.contrib.auth import authenticate, login

user = authenticate(request, username='username', password='password')
if user is not None:
    login(request, user)
else:
    # 驗證失敗的處理
```

`authenticate()` 函數會檢查用戶名和密碼是否正確，並返回一個用戶對象 (User instance) 或 `None`。

---

## **(2) 調用 `login()` 函數**
當用戶通過身份驗證後，`login()` 函數會執行以下步驟：

1. **綁定用戶到 session**  
   - Django 使用 session 框架來管理用戶的登入狀態。
   - `login()` 函數會將用戶的主鍵 (Primary Key) 存儲到 session 中，鍵名為 `_auth_user_id`。
   - 同時，還會存儲用戶的後端信息 (`_auth_user_backend`)，用於標記是哪個身份驗證後端處理了該用戶。

   **相關代碼片段：**
   ```python
   request.session[SESSION_KEY] = user.pk  # 存儲用戶主鍵
   request.session[BACKEND_SESSION_KEY] = user.backend  # 存儲後端信息
   ```

2. **設置 Cookie**  
   - Django 的 session 框架會自動將 session ID 存儲到用戶的瀏覽器 Cookie 中。
   - 這個 Cookie 的名稱默認為 `sessionid`，可以在 `settings.SESSION_COOKIE_NAME` 中自定義。
   - 當用戶發送後續請求時，瀏覽器會自動攜帶這個 Cookie，Django 會根據 Cookie 中的 session ID 找到對應的 session 數據。

3. **更新 `request.user`**  
   - `login()` 函數會將 `request.user` 更新為當前登入的用戶對象。
   - 這樣，後續的請求中可以通過 `request.user` 獲取當前用戶的相關信息。

---

## **(3) 驗證用戶狀態**
在後續的請求中，Django 會自動驗證用戶的登入狀態：

1. **從 Cookie 中提取 session ID**  
   - 當用戶發送請求時，Django 會從請求的 Cookie 中提取 session ID，並查找對應的 session 數據。

2. **加載用戶對象**  
   - 如果 session 中存在 `_auth_user_id`，Django 會根據該 ID 從數據庫中加載用戶對象，並將其設置為 `request.user`。

3. **驗證用戶是否已登入**  
   - 可以通過 `request.user.is_authenticated` 判斷用戶是否已登入。

---

# 3. **完整流程圖**

1. 用戶提交登入表單 (包含用戶名和密碼)。
2. 後端調用 `authenticate()` 驗證用戶身份。
3. 如果驗證成功，調用 `login()`：
   - 將用戶 ID 存入 session。
   - 設置 session ID 到 Cookie。
   - 更新 `request.user`。
4. 後續請求中，Django 根據 Cookie 驗證用戶身份。

---

# 4. **相關設置**

- **session 存儲方式**  
  Django 默認使用數據庫存儲 session 數據，可以通過 `SESSION_ENGINE` 配置更改：
  ```python
  SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 默認使用數據庫
  ```

- **Cookie 配置**  
  可以通過以下設置自定義 Cookie 行為：
  ```python
  SESSION_COOKIE_NAME = 'sessionid'  # Cookie 名稱
  SESSION_COOKIE_AGE = 1209600  # Cookie 有效期（秒）
  SESSION_COOKIE_SECURE = True  # 僅在 HTTPS 下傳輸
  ```

---

# 5. **注意事項**

- **`request.user` 的使用**  
  - `request.user` 是一個 `User` 對象或 `AnonymousUser` 對象。
  - 可以通過 `request.user.is_authenticated` 判斷用戶是否已登入。

- **登出處理**  
  使用 `logout()` 函數可以清除 session 數據並登出用戶：
  ```python
  from django.contrib.auth import logout

  logout(request)
  ```

---

# 6. **範例代碼**

以下是一個完整的登入流程範例：

```python
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # 登入成功後跳轉
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # 登出後跳轉
```

---

# 7. **結論**
Django 的 `login()` 函數通過 session 和 Cookie 管理用戶的登入狀態，並提供了方便的 `request.user` 接口來驗證用戶身份。理解其運作流程有助於開發安全且高效的用戶認證系統。