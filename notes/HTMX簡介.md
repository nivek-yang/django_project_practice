---
title: HTMX 簡介
date: 2025-04-29
categories:
  - [技術筆記]
tags:
  - HTMX
---

HTMX 是一個輕量級的前端框架，允許開發者直接在 HTML 中使用屬性來實現動態交互，無需撰寫大量的 JavaScript。它支持使用標準的 HTTP 方法（GET、POST、PUT、DELETE）進行局部更新，並且可以與 Django 等後端框架無縫整合。

---

# HTMX 的核心功能

## 1. **局部更新**
HTMX 可以通過 `hx-get` 或 `hx-post` 等屬性發送請求，並將返回的 HTML 片段插入到指定的 DOM 節點中。

### 範例：按讚功能
```html
{% if user in interview.favorited_by.all %}
    <button hx-swap="outerHTML" hx-post="{% url 'interviews:favorite' interview.id %}" class="btn btn-primary">已收藏</button>
{% else %}
    <button hx-swap="outerHTML" hx-post="{% url 'interviews:favorite' interview.id %}" class="btn btn-ghost">收藏</button>
{% endif %}
```

- **`hx-post`**: 發送 POST 請求到指定的 URL。
- **`hx-swap="outerHTML"`**: 替換按鈕本身的 HTML，而不僅僅是其內部內容。

---

## 2. **動態載入內容**
HTMX 支持在用戶操作時動態載入內容，例如模態視窗（Modal）。

### 範例：動態載入模態視窗
```html
<button hx-get="/modal" hx-target="#modal-container" class="btn">打開模態視窗</button>

<div id="modal-container"></div>
```

- **`hx-get`**: 發送 GET 請求到 `/modal`。
- **`hx-target`**: 指定將返回的 HTML 插入到 `#modal-container` 中。

---

## 3. **表單提交**
HTMX 可以用於處理表單提交，並動態更新頁面的一部分。

### 範例：新增留言
```html
<form action="{% url 'interviews:comment' interview.id %}" method="post" hx-target=".list" hx-swap="beforeend">
    {% csrf_token %}
    <textarea name="content"></textarea>
    <button>新增留言</button>
</form>
```

- **`hx-target`**: 指定將返回的內容插入到 `.list` 元素中。
- **`hx-swap="beforeend"`**: 將返回的內容追加到 `.list` 的末尾。

---

## 4. **事件處理**
HTMX 支持使用屬性來處理事件，例如在請求完成後執行操作。

### 範例：顯示成功訊息
```html
<button hx-post="/action" hx-trigger="click" hx-on="htmx:afterRequest: alert('操作成功')">執行操作</button>
```

- **`hx-trigger`**: 指定觸發請求的事件。
- **`hx-on`**: 綁定 HTMX 事件（如 `htmx:afterRequest`）並執行 JavaScript。

---

# HTMX 與 Django 的整合

## 1. **後端返回部分模板**
在 Django 視圖中，返回一部分模板作為 HTMX 的響應。

### 範例：按讚視圖

views.py
```python
@require_POST
@login_required
def favorite(req, id):
    interview = get_object_or_404(Interview, pk=id)
    favorites = req.user.favorite_interviews

    if favorites.filter(pk=interview.pk).exists():
        favorites.remove(interview)
    else:
        favorites.add(interview)

    return render(req, "interviews/favorite.html", {"user": req.user, "interview": interview})
```

favorite.html
```html
{% if user in interview.favorited_by.all %}
    <button hx-swap="outerHTML" hx-post="{% url 'interviews:favorite' interview.id %}" class="btn btn-primary" >已收藏</button>
{% else %}
    <button hx-swap="outerHTML" hx-post="{% url 'interviews:favorite' interview.id %}" class="btn btn-ghost" >收藏</button>
{% endif %}
```

- 視圖返回的模板只包含按鈕的 HTML，HTMX 會自動更新頁面。

---

## 2. **CSRF Token**
HTMX 請求需要包含 CSRF Token，否則 Django 會拒絕請求。

### 解決方法
在 HTML 的 `<body>` 標籤中添加以下屬性：
```html
<body hx-headers='{"x-csrftoken": "{{ csrf_token }}"}'>
```

---

## 3. **局部渲染**
HTMX 可以用於實現局部渲染，避免整頁刷新。

### 範例：留言列表

```html
<form action="{% url 'interviews:comment' interview.id %}" method="post" hx-target=".list" hx-swap="beforeend">
    {% csrf_token %}
    <textarea name="content"></textarea>
    <button>新增留言</button>
</form>
```

```html
<ul class="list">
    {% for comment in comments %}
    <li>
        <p>{{ comment.user }} 說：{{ comment.content }}</p>
    </li>
    {% endfor %}
</ul>
```

- 新增留言後，HTMX 只更新 `.list` 的內容，而不是整個頁面。

---

# HTMX 的優勢

1. **簡化前端開發**: 無需撰寫大量 JavaScript，直接在 HTML 中定義交互邏輯。
2. **與後端無縫整合**: 使用 Django 模板引擎生成 HTML，減少前後端分離的複雜性。
3. **提升性能**: 支持局部更新，減少不必要的頁面刷新。

---

# HTMX 的限制

1. **複雜交互**: 對於需要大量前端邏輯的應用，HTMX 可能不如前端框架（如 React 或 Vue）靈活。
2. **學習曲線**: 雖然 HTMX 簡單，但需要熟悉其屬性和事件。

---

# 總結
HTMX 是一個強大且輕量的工具，適合用於需要快速開發的 Django 項目。通過 HTMX，可以實現高效的局部更新和動態交互，提升用戶體驗，同時保持代碼的簡潔性。