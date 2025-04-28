---

### 如何處理「動態切換按讚狀態」並使用 `ManyToMany` 關聯模型

---

在本筆記中，我們將探討如何在 Django 中處理「動態切換按讚狀態」的邏輯。具體而言，我們會：

1. **介紹 `ManyToMany` 關聯模型的建立**，並解釋如何使用它來設置使用者與面試（`Interview`）之間的關聯。
2. **說明為何在這樣的情境下，不能使用 `get_object_or_404()`**，而是應該使用 `filter()` 方法來處理查詢。
3. **展示如何在 `favorite` 這樣的 view function 中實現按讚功能**，並且如何動態切換按讚狀態。

---

## 1. `ManyToMany` 關聯模型的建立

在 Django 中，使用 `ManyToMany` 關聯來表示多對多的關係。假設我們有一個 `User` 和 `Interview` 模型，我們可以建立以下的多對多關聯：

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

### 關聯設置
- **`FavoriteInterview`** 表示每個使用者對於某個訪談的「按讚」記錄。每一筆記錄由 `user` 和 `interview` 兩個外鍵組成。
- **`unique_together`** 確保每個使用者對同一篇訪談只有一個按讚記錄。

### 使用 `ManyToManyField`
假設我們希望在 `User` 模型中表示使用者按讚過的所有 `Interview`，我們可以在 `Interview` 模型中設置 `ManyToManyField` 來表示這種關聯：

```python
class Interview(models.Model):
    # 其他欄位...
    favorited_by = models.ManyToManyField(
        User,
        through="FavoriteInterview",
        related_name="favorite_interviews"
    )
```

這樣，我們就可以通過 `interview.favorited_by` 來獲取按讚這篇面試的所有使用者
也可以通過 `user.favorite_interviews` 來獲取使用者按讚的所有面試

---

## 2. 為何不能使用 `get_object_or_404()`，要用 `filter()`

### `get_object_or_404()` 的限制
`get_object_or_404()` 是 Django 中常用的查詢方法，目的是在查詢不到資料時，自動拋出 `Http404` 錯誤。它的常見用法是：

```python
from django.shortcuts import get_object_or_404

# 假設我們想獲取某個 Interview
interview = get_object_or_404(Interview, pk=interview_id)
```

然而，**在動態切換按讚狀態的情境中，這並不適用**。原因如下：

- **不能處理不存在的關聯**：如果使用 `get_object_or_404()`，當用戶試圖對尚未按讚的訪談進行「取消按讚」操作時，會引發 404 錯誤，這是我們不希望的行為。因為當使用者尚未按讚，查詢不到 `FavoriteInterview` 記錄並不代表資源不存在，而只是表明使用者尚未按讚。
  
- **不易控制流程**：如果使用 `get_object_or_404()`，我們無法根據查詢結果靈活地處理後續邏輯，比如判斷是否已經按讚，並根據狀況決定是添加還是刪除關聯。

### 使用 `filter()` 解決問題
`filter()` 方法可以返回符合條件的查詢結果，如果沒有找到任何符合條件的資料，它會返回一個空的 queryset，而不是拋出錯誤。因此，`filter()` 使得我們可以靈活處理按讚的狀態：

```python
if user.favorite_interviews.filter(pk=interview.pk).exists():
    # 如果已經按過讚，則取消按讚
    user.favorite_interviews.remove(interview)
else:
    # 如果沒按過讚，則新增按讚
    user.favorite_interviews.add(interview)
```

這樣寫可以讓我們**動態判斷**使用者是否已經按讚，並且根據結果執行相應的操作。

---

## 3. 在 `favorite` view function 中的使用方式

下面是 `favorite` view function 的完整範例，它展示了如何處理「按讚」和「取消按讚」的邏輯：

```python
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@require_POST
@login_required
def favorite(req, id):
    interview = get_object_or_404(Interview, pk=id)  # 獲取指定的 interview
    user = req.user  # 獲取當前使用者

    # 判斷這位使用者是否已經按過讚
    if user.favorite_interviews.filter(pk=interview.pk).exists():
        # 如果已經按過讚，則取消按讚（remove）
        user.favorite_interviews.remove(interview)
    else:
        # 如果沒有按過讚，則新增按讚（add）
        user.favorite_interviews.add(interview)

    # 重定向回該頁面，通常是顯示這個 interview 的詳細頁面
    return redirect("interviews:show", id=interview.id)
```

### 功能解釋：
- **`get_object_or_404()`**：查找指定的 `Interview` 實例，若找不到則會拋出 404 錯誤（這裡是確保該訪談存在）。
- **`filter(pk=interview.pk).exists()`**：檢查該 `user` 是否已經按讚過這篇 `interview`，如果已經按讚，則執行 `remove()`；如果沒有按讚，則執行 `add()`，這樣就能夠動態切換按讚狀態。
- **`redirect()`**：操作完成後，重定向回該 `interview` 的詳細頁面。

---

### 小結

1. **`ManyToMany` 關聯的建立**：我們使用 `ManyToManyField` 和 `through` 參數來設置 `User` 和 `Interview` 之間的多對多關聯，並且在中介模型 `FavoriteInterview` 中存儲按讚資料。
   
2. **為何不使用 `get_object_or_404()`**：在動態切換按讚狀態時，使用 `get_object_or_404()` 不適合，因為它會拋出 404 錯誤，這會讓我們無法靈活處理「已按讚」和「未按讚」的情況。

3. **使用 `filter()` 判斷狀態**：使用 `filter()` 和 `.exists()` 來檢查 `FavoriteInterview` 是否存在對應的關聯，根據結果決定是添加還是移除按讚。

這樣的設計確保了按讚功能的靈活性和安全性，並且符合 Django 的最佳實踐。

---

希望這篇技術筆記有幫助，如果你有其他問題，隨時告訴我！😊