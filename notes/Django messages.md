---
title: Django Messages 快閃訊息的運作機制
date: 2025-04-30
categories:
  - [技術筆記]
tags:
  - Python
  - Django
---

# 什麼是 Django Messages？
Django 提供了一個內建的訊息框架（`django.contrib.messages`），用於在請求之間傳遞提示訊息，這些訊息通常用於通知使用者某些操作的結果，例如成功、錯誤或警告等。這類訊息被稱為 **「快閃訊息」（Flash Messages）**，因為它們只會在下一次請求中顯示，然後自動消失。

---

# 使用場景
Django Messages 適合用於以下場景：
- 表單提交成功或失敗的提示。
- 操作完成後的通知（例如：資料已儲存、刪除成功）。
- 錯誤或警告訊息的顯示。

---

# 快閃訊息的類型
Django 提供了以下內建的訊息類型：
- **`messages.debug`**: 用於調試訊息。
- **`messages.info`**: 一般資訊提示。
- **`messages.success`**: 成功訊息。
- **`messages.warning`**: 警告訊息。
- **`messages.error`**: 錯誤訊息。

---

# 如何使用 Django Messages？

## 1. **啟用 Messages**
確保 `django.contrib.messages` 已包含在 `INSTALLED_APPS` 中，並且模板中已載入 `messages` 中間件。

`settings.py`:
```python
INSTALLED_APPS = [
    ...
    'django.contrib.messages',
    ...
]

MIDDLEWARE = [
    ...
    'django.contrib.messages.middleware.MessageMiddleware',
    ...
]
```

---

## 2. **在視圖中添加訊息**
使用 `messages` 模組在視圖中添加訊息。

範例：
```python
from django.contrib import messages
from django.shortcuts import redirect

def my_view(request):
    # 添加成功訊息
    messages.success(request, "操作成功！")
    # 添加警告訊息
    messages.warning(request, "這是警告訊息！")
    return redirect("home")
```

---

## 3. **在模板中顯示訊息**
在模板中使用 `messages` 模板標籤來顯示訊息。

範例：
```html
{% if messages %}
    <ul class="messages">
        {% for message in messages %}
            <li class="{{ message.tags }}">{{ message }}</li>
        {% endfor %}
    </ul>
{% endif %}
```

- **`message.tags`**: 自動添加的 CSS 樣式類型（如 `success`、`warning`）。
- **`message`**: 訊息的內容。

---

## 4. **自訂樣式**
可以根據訊息類型自訂樣式，提升用戶體驗。

範例（CSS）：
```css
.messages {
    list-style: none;
    padding: 0;
}

.messages .success {
    color: green;
}

.messages .warning {
    color: orange;
}

.messages .error {
    color: red;
}
```

---

# 完整範例

以下是使用 DaisyUI 和 Alpine.js 實現的完整範例，包含可點擊 `x` 按鈕關閉訊息的功能，並根據訊息類型（如 `success`、`warning`、`error`）自動套用樣式：

```html
{% if messages %}
    {% for message in messages %}
        <template x-data="{show: true}" x-if="show">
            <div role="alert" class="alert alert-{{ message.tags }}">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 shrink-0 stroke-current" fill="none" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>{{ message }}</span>
                <button @click="show = false" class="btn btn-xs">x</button>
            </div>
        </template>
    {% endfor %}
{% endif %}
```

---

## 功能說明

1. **Alpine.js 的 `x-data` 和 `x-if`**:
   - 使用 `x-data="{ show: true }"` 初始化訊息的顯示狀態。
   - 使用 `x-if="show"` 控制訊息是否顯示，點擊 `x` 按鈕後將 `show` 設為 `false`，隱藏訊息。

2. **DaisyUI 的 `alert` 樣式**:
   - 使用 `alert` 類別來套用 DaisyUI 的樣式。
   - 根據 `message.tags` 動態添加樣式類別（如 `alert-success`、`alert-warning`、`alert-error` 等）。
s
3. **關閉按鈕**:
   - 使用 DaisyUI 的按鈕樣式 `btn btn-xs btn-circle btn-outline`。
   - 點擊按鈕時，透過 Alpine.js 的 `@click` 事件隱藏訊息。

---

## Alpine.js 和 DaisyUI 的引入

1. **Alpine.js 的引入**:
   確保在模板中已經引入 Alpine.js CDN：
   ```html
   <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
   ```

2. **DaisyUI 的安裝**:
   DaisyUI 是基於 Tailwind CSS 的元件庫，確保已正確安裝並配置 Tailwind 和 DaisyUI。
---

這樣的設計不僅美觀，還能提供良好的用戶體驗，適合用於各種 Django 項目中需要提示訊息的場景。


# 注意事項
1. **訊息的持久性**:
   - Django Messages 預設只會在下一次請求中顯示，之後會自動清除。
   - 如果需要更長時間的訊息顯示，可以考慮自訂訊息存儲（`Message Storage`）。

2. **訊息存儲後端**:
   - 預設使用 `CookieStorage` 或 `SessionStorage`。
   - 可以在 `settings.py` 中自訂：
     ```python
     MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
     ```

3. **多條訊息顯示**:
   - 如果在同一個請求中添加多條訊息，`messages` 會以列表的形式顯示。

---

# 總結
Django Messages 是一個簡單而強大的工具，適合用於提示訊息的顯示。通過內建的訊息類型和模板標籤，可以快速實現用戶友好的通知功能，並提升應用的交互體驗。