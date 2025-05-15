---
title: Django 使用 `ManyToMany` 關聯模型處理「動態切換按讚狀態」
date: 2025-04-23
categories:
  - [技術筆記]
tags:
  - Python
  - Django
  - Database
---



---

在本筆記中，將探討如何在 Django 中處理「動態切換按讚狀態」的邏輯:

1. **介紹 `ManyToMany` 關聯模型的建立**，並解釋如何使用它來設置使用者 (`User`) 與面試（`Interview`）之間的關聯。
2. **說明為何在這樣的情境下，不能使用 `get_object_or_404()`**，而是應該使用 `filter()` 方法來處理查詢。
3. **展示如何在 `favorite` 這樣的 view function 中實現按讚與取消按讚功能**，動態切換按讚狀態。

---

# `ManyToMany` 關聯模型的建立

在 Django 中，使用 `ManyToMany` 關聯來表示多對多的關係。假設有 `User` 和 `Interview` 模型，可以建立以下的多對多關聯：

interviews/models.py
```python
from django.contrib.auth.models import User
from django.db import models

class Interview(models.Model):
    # 其他欄位...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(
        User,
        through="FavoriteInterview",
        related_name="favorite_interviews",  # join 欄位
    )

# join table
class FavoriteInterview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
```

## 關聯設置
- **`FavoriteInterview`** 表示每個使用者對於某個面試的「按讚」記錄。每一筆記錄由 `user` 和 `interview` 兩個外鍵組成。

## 使用 `ManyToManyField`
假設希望在 `User` 模型中表示使用者按讚過的所有 `Interview`，可以在 `Interview` 模型中設置 `ManyToManyField` 來表示這種關聯

- 通過 `interview.favorited_by` 來獲取按讚某篇面試的所有使用者
- 通過 `user.favorite_interviews` 來獲取某位使用者按讚的所有面試

---


## 在 `favorite` view function 中處理「按讚」和「取消按讚」的邏輯

interviews/views.py
```python
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@require_POST
@login_required
def favorite(req, id):
    interview = get_object_or_404(Interview, pk=id)  # 獲取指定的 interview
    favorites = req.user.favorite_interviews # 登入的 user 按讚的所有面試

    # 以 User model 的角度處理 ManyToMany 關聯
    # 判斷這位使用者是否已經按過讚
    if favorites.filter(pk=interview.pk).exists():
        # 如果有按過讚，則取消按讚（remove），在 FavoriteInterview table 裡刪除該筆資料
        favorites.remove(interview) 
    else:
        # 如果沒有按過讚，則加上（add)，在 FavoriteInterview table 裡增加該筆資料
        favorites.add(interview)

    return redirect("interviews:show", id=interview.id)
```

## 功能解釋：
- **`get_object_or_404()`**：查找指定的 `Interview` 實例，若找不到則會拋出 404 錯誤（這裡是確保該面談存在）。
- **`filter(pk=interview.pk).exists()`**：檢查該 `user` 是否已經按讚過這篇 `interview`，如果已經按讚，則執行 `remove()`；如果沒有按讚，則執行 `add()`，這樣就能夠動態切換按讚狀態。
- **`redirect()`**：操作完成後，重定向回該 `interview` 的詳細頁面。

---

## 小結

1. **`ManyToMany` 關聯的建立**：使用 `ManyToManyField` 和 `through`、`related_name` 參數來設置 `User` 和 `Interview` 之間的多對多關聯，並且在中介模型 `FavoriteInterview` 中存儲按讚資料。
   
2. **使用 `filter()` 判斷使用者是否已經按過讚**：使用 `filter()` 和 `.exists()` 來檢查 `FavoriteInterview` 是否存在對應的關聯，根據結果決定是按讚還是移除按讚。
`filter()` 方法可以返回符合條件的查詢結果，如果沒有找到任何符合條件的資料，它會返回一個空的 queryset，而不是拋出錯誤，因此`filter()` 可以靈活處理按讚的狀態

3. **為何 `get_object_or_404()` 不適用判斷使用者是否已經按過讚**：在動態切換按讚狀態時，使用 `get_object_or_404()` 不適合，因為查詢結果沒有找到資料，它會拋出 404 錯誤，這會讓我們無法靈活處理「已按讚」和「未按讚」的情況。

---

## 從不同 Model 角度處理 `ManyToMany` 關聯

在 Django 中，`ManyToMany` 關聯允許兩個模型之間建立多對多的關聯。這些關聯通常由 `ManyToManyField` 或透過額外的關聯表（如 `through` 設定）來實現。在不同的 Model 角度處理 `ManyToMany` 關聯時，我們有不同的寫法來處理關聯資料的新增、刪除與查詢。

### 1. **從 `User` 模型的角度處理 `ManyToMany` 關聯**

首先，讓我們回顧如何從 `User` 模型的角度處理 `ManyToMany` 關聯。在這個例子中，`User` 和 `Interview` 之間的關聯是透過 `favorite_interviews`（即 `ManyToManyField`）來建立的。我們可以在 `User` 模型上使用 `favorite_interviews`，來處理這篇 `Interview` 是否已經被使用者按讚過。

```python
@require_POST
@login_required
def favorite(req, id):
    interview = get_object_or_404(Interview, pk=id)
    user = req.user

    # 以 User model 的角度處理 ManyToMany 關聯
    # 判斷這位使用者是否已經按過讚
    if user.favorite_interviews.filter(pk=interview.pk).exists():
        # 如果有按過讚，則取消按讚（remove）
        user.favorite_interviews.remove(interview)
    else:
        # 如果沒有按過讚，則加上（add）
        user.favorite_interviews.add(interview)
```

- `user.favorite_interviews.filter(pk=interview.pk)`：我們通過 `filter` 查詢使用者是否已經對這篇 `interview` 按讚過，這會返回一個 `QuerySet`，並且使用 `exists()` 方法檢查是否存在此條記錄。
- `remove()` 和 `add()`：`remove()` 用來移除使用者對該 `interview` 的按讚記錄，`add()` 用來新增按讚記錄。

### 2. **從 `Interview` 模型的角度處理 `ManyToMany` 關聯**

另一種處理方式是從 `Interview` 模型的角度來管理 `ManyToMany` 關聯。可以直接操作 `favorited_by`，這是 `Interview` 模型中的 `ManyToManyField`，它用來表示所有按讚過這篇訪談的使用者。

```python
    # 以 Interview model 的角度處理 ManyToMany 關聯
    # 判斷這篇文章是否已經被按過讚
    if interview.favorited_by.filter(pk=user.pk).exists():
        # 如果有按過讚，則取消按讚（remove）
        interview.favorited_by.remove(user)
    else:
        # 如果沒有按過讚，則加上（add）
        interview.favorited_by.add(user)
```

- `interview.favorited_by.filter(pk=user.pk)`：使用 `filter` 查詢是否該 `user` 已經按讚過這篇 `interview`，如果有，則移除按讚；如果沒有，則將按讚關聯添加回 `favorited_by`。

### 3. **從 `FavoriteInterview` 模型的角度處理 `ManyToMany` 關聯**

如果我們使用的是 `through` 設定的 `ManyToMany` 關聯（在本例中，使用了 `FavoriteInterview` 作為關聯模型），可以直接操作 `FavoriteInterview` 模型來添加或刪除按讚記錄。

```python
    # 以 FavoriteInterview model 的角度處理 ManyToMany 關聯
    favorite_interview = FavoriteInterview.objects.filter(user=user, interview=interview)

    if favorite_interview.exists():
        # 如果已經按過讚，則刪除該記錄
        favorite_interview.delete()
    else:
        # 如果沒有按過讚，則新增該記錄
        FavoriteInterview.objects.create(user=user, interview=interview)
```

- 首先查詢是否已經存在這個 `FavoriteInterview` 記錄，如果存在則刪除（使用 `.delete()`），如果不存在則創建新的 `FavoriteInterview` 記錄（使用 `.create()`）。
  
- 使用 `filter(user=user, interview=interview)` 來確保我們只關注到該使用者和該訪談的關聯。

## 總結：
- **`ManyToManyField`** 在 Django 可以用來管理多對多的關聯。但當需要處理這些關聯時，必須明確知道該如何從不同的角度來操作。
  - **從 `User` 模型的角度**：我們可以操作該使用者的 `favorite_interviews` 屬性來添加或移除關聯。
  - **從 `Interview` 模型的角度**：我們可以操作該面試的 `favorited_by` 屬性來處理關聯。
  - **從 `FavoriteInterview` 模型的角度**：透過 `through` 設定的關聯表，可以直接操作這個模型來進行新增或刪除。

這些方法各有其使用場景，選擇哪一種方式取決於你的需求和數據模型的設計。在處理 `ManyToMany` 關聯時，要特別注意數據一致性和簡潔性，並選擇最符合需求的解決方案。