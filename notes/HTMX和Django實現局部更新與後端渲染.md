---
title: HTMX 與 Django 實現局部更新與後端渲染
date: 2025-04-29
categories:
  - [技術筆記]
tags:
  - HTMX
---


# 功能概述
此功能實現了一個按讚（收藏）按鈕，使用者可以對特定的項目（如面試記錄）進行按讚或取消按讚操作。按鈕的狀態（已收藏或收藏）由後端決定，並通過 HTMX 局部更新頁面。

---

# 技術細節

## 1. **前端模板設計**

### favorite.html
這個模板負責渲染按讚按鈕，按鈕的狀態根據使用者是否已經按讚來決定。

```html
{% if user in interview.favorited_by.all %}
    <button hx-swap="outerHTML" hx-post="{% url 'interviews:favorite' interview.id %}" class="btn btn-primary" >已收藏</button>
{% else %}
    <button hx-swap="outerHTML" hx-post="{% url 'interviews:favorite' interview.id %}" class="btn btn-ghost" >收藏</button>
{% endif %}
```

- **`hx-post`**: 當按鈕被點擊時，發送一個 POST 請求到指定的 URL。
- **`hx-swap="outerHTML"`**: 指定 HTMX 替換整個按鈕的 HTML，而不僅僅是按鈕內的內容。
- **按鈕狀態**: 使用 Django 模板語法 `{% if user in interview.favorited_by.all %}` 判斷使用者是否已按讚，並渲染不同的按鈕樣式和文字。
  
> 如果沒有指定 `hx-target`，HTMX 預設會將後端返回的內容插入到觸發請求的元素本身內部，並替換其內部內容（即 `innerHTML`）。這是 HTMX 的默認行為

---

### `show.html`
在主頁面中，通過 `include` 將 favorite.html 嵌入到頁面中，並用 `with` 傳遞變數。

```html
{% include 'interviews/favorite.html' with user=user interview=interview %}
```

- **`include`**: 將 favorite.html 作為子模板嵌入。
- **`with`**: 傳遞變數 `user` 和 `interview`，供子模板使用。

---

## 2. **後端邏輯**

### `views.py`
後端處理按讚請求，並返回更新後的按鈕 HTML。

```python
@require_POST
@login_required
def favorite(req, id):
    interview = get_object_or_404(Interview, pk=id)
    favorites = req.user.favorite_interviews

    # 判斷使用者是否已按讚
    if favorites.filter(pk=interview.pk).exists():
        # 如果已按讚，則取消按讚
        favorites.remove(interview)
    else:
        # 如果未按讚，則新增按讚
        favorites.add(interview)
    
    # 返回更新後的按鈕 HTML
    return render(req, "interviews/favorite.html", {"user": req.user, "interview": interview})
```

- **`require_POST`**: 限制此視圖僅接受 POST 請求。
- **`login_required`**: 確保只有已登入的使用者可以執行按讚操作。
- **按讚邏輯**:
  - 使用 `ManyToMany` 關聯的 `filter` 方法檢查使用者是否已按讚。
  - 如果已按讚，則移除關聯（`remove`）；否則，新增關聯（`add`）。
- **返回模板**: 使用 `render` 返回更新後的 favorite.html，HTMX 會自動將其插入到頁面中。

---

## 3. **HTMX 的作用**
HTMX 在這裡負責處理按鈕的動態更新，無需整頁刷新。

- **請求發送**: 當按鈕被點擊時，HTMX 發送一個 POST 請求到後端。
- **局部更新**: 後端返回的 HTML 片段（`favorite.html`）會替換按鈕的 HTML，實現按鈕狀態的即時更新。

---

# 流程總結

1. **頁面初始渲染**:
   - 在 `show.html` 中包含 favorite.html，按鈕的初始狀態由後端決定。

2. **按鈕點擊**:
   - 使用者點擊按鈕時，HTMX 發送一個 POST 請求到後端的 `favorite` 視圖。

3. **後端處理請求**:
   - 後端檢查使用者是否已按讚，並執行相應的新增或移除操作。
   - 返回更新後的按鈕 HTML。

4. **前端更新**:
   - HTMX 接收後端返回的 HTML，並使用 `hx-swap="outerHTML"` 替換按鈕的 HTML，實現即時更新。

---

# 優勢分析

1. **簡化前端邏輯**:
   - 無需撰寫額外的 JavaScript，所有交互邏輯都由 HTMX 和 Django 模板處理。

2. **提升性能**:
   - 使用 HTMX 的局部更新功能，避免整頁刷新，提升用戶體驗。

3. **後端驅動渲染**:
   - 按鈕狀態由後端決定，確保資料一致性，減少前後端同步的複雜性。

---

# 注意事項

1. **CSRF Token**:
   - 確保 HTMX 請求包含 CSRF Token，否則 Django 會拒絕請求。
   - 可以在 `<body>` 標籤中添加：
     ```html
     <body hx-headers='{"x-csrftoken": "{{ csrf_token }}"}'>
     ```

2. **錯誤處理**:
   - 如果後端操作失敗，應返回適當的錯誤訊息，並在前端顯示。

---

# 總結
此功能結合了 HTMX 和 Django 的優勢，實現了一個高效、簡潔的按讚功能。HTMX 的局部更新特性使得頁面交互更加流暢，而 Django 的後端渲染確保了資料的一致性與安全性。