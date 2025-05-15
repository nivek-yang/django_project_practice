---
title: N+1 問題與解決方法
date: 2025-05-01
categories:
  - [技術筆記]
tags:
  - SQL
  - Django
  - Python
---


# 什麼是 N+1 問題？

> **N+1 問題** 是一種常見的效能問題，通常發生在處理資料庫查詢時。當我們需要查詢一個主物件及其相關聯的子物件時，程式會執行 1 次查詢來獲取主物件，然後為每個主物件執行 N 次查詢來獲取其相關聯的子物件。這樣總共會執行 **1 + N** 次查詢，導致效能低下。

---

# 什麼時候會發生 N+1 問題？

1. **關聯查詢**：
   - 當模型之間有外鍵（`ForeignKey`）、一對一（`OneToOneField`）或多對多（`ManyToManyField`）關聯時，容易發生 N+1 問題。

2. **模板中迴圈訪問關聯物件**：
   - 在模板中使用迴圈訪問關聯物件時，可能會導致多次查詢。

   範例：
   ```django-html
   {% for comment in comments %}
       {{ comment.author.name }}
   {% endfor %}
   ```

---

## 範例：留言與作者 (多對一)

假設我們有一個留言系統，每條留言都有一個作者。當我們需要顯示所有留言及其作者時，可能會發生 N+1 問題。

1. **查詢留言**：執行 1 次查詢來獲取所有留言。
   ```sql
   SELECT * FROM comments;
   ```

2. **查詢作者**：對於每條留言，執行 1 次查詢來獲取該留言的作者。
   ```sql
   SELECT * FROM users WHERE id = <author_id>;
   ```

如果有 100 條留言，總共會執行 **1 + 100 = 101 次查詢**。

---

# N+1 問題的影響

- **效能低下**：大量的查詢會增加資料庫的負載，特別是在高流量的應用中。
- **延遲增加**：每次查詢都需要與資料庫交互，導致頁面加載時間變長。

---

# 解決方法

## 1. **使用 `select_related`**
`select_related` 用於解決 **一對一** 或 **多對一** 關聯的 N+1 問題。它會在一次查詢中使用 SQL 的 `JOIN`，將相關聯的資料一起查出來。

### 範例 (多對一)：
```python
# N+1 問題
comments = Comment.objects.all()
for comment in comments:
    print(comment.author.name)  # 每次訪問 author 都會執行一次查詢

# 解決 N+1 問題
comments = Comment.objects.select_related('author')
for comment in comments:
    print(comment.author.name)  # 不會再執行額外的查詢
```

- 使用 `select_related`，Django 在查詢留言時，會同時透過 SQL 的 `JOIN` 將留言和作者的資料一起查出來。

### SQL 查詢：
```sql
SELECT comments.*, users.*
FROM comments
JOIN users ON comments.author_id = users.id;
```

---

### **SQL 查詢對比**

| 方法                  | 查詢次數 | SQL 查詢範例                                                                 |
|-----------------------|----------|------------------------------------------------------------------------------|
| **N+1 問題**          | 1 + N    | 1. `SELECT * FROM comments;` <br> 2. `SELECT * FROM users WHERE id = <id>;` |
| **使用 `select_related`** | 1        | `SELECT comments.*, users.* FROM comments JOIN users ON comments.author_id = users.id;` |


---

## 2. **使用 `prefetch_related`**
`prefetch_related` 用於解決 **一對多** 或 **多對多** 關聯的 N+1 問題。它會執行兩次查詢，並在 Python 中將結果關聯起來。

### 範例 (一對多)：
```python
# N+1 問題
authors = Author.objects.all()
for author in authors:
    print(author.books.all())  # 每次訪問 books 都會執行一次查詢

# 解決 N+1 問題
authors = Author.objects.prefetch_related('books')
for author in authors:
    print(author.books.all())  # 不會再執行額外的查詢
```

- `prefetch_related` 會執行兩次查詢：
    1. 查詢所有作者。
    2. 查詢所有書籍，並在 Python 中將書籍與對應的作者關聯起來。

### SQL 查詢：
```sql
SELECT * FROM authors;
SELECT * FROM books WHERE author_id IN (<author_ids>);
```

### **SQL 查詢對比**

| 方法                  | 查詢次數 | SQL 查詢範例                                                                 |
|-----------------------|----------|------------------------------------------------------------------------------|
| **N+1 問題**          | 1 + N    | 1. `SELECT * FROM authors;` <br> 2. `SELECT * FROM books WHERE author_id = <author_id>;` |
| **`prefetch_related`** | 2        | 1. `SELECT * FROM authors;` <br> 2. `SELECT * FROM books WHERE author_id IN (<author_ids>);` |

--- 

#### **N+1 問題的查詢（使用 `=`）**
```sql
SELECT * FROM books WHERE author_id = 1;
SELECT * FROM books WHERE author_id = 2;
SELECT * FROM books WHERE author_id = 3;
```
- 每次查詢只匹配一個 `author_id`，需要執行多次查詢（N 次）。

#### **`prefetch_related` 的查詢（使用 `IN`）**
```sql
SELECT * FROM books WHERE author_id IN (1, 2, 3);
```
- 一次查詢即可匹配多個 `author_id`，大幅減少查詢次數。

> 在解決 N+1 問題時，`prefetch_related` 使用 `IN`，可以一次查詢多個關聯物件，顯著提升效能

---

### select_related 與 prefetch_related 的比較

select_related 和 prefetch_related 是 Django 中用來解決 N+1 問題的兩個方法，但它們適用於不同的場景，且工作方式也不同

| 特性                  | `select_related`                     | `prefetch_related`                  |
|-----------------------|---------------------------------------|--------------------------------------|
| 適用關係              | 多對一、一對一                       | 一對多、多對多                       |
| 查詢次數              | 1 次查詢                             | 2 次查詢                             |
| 工作方式              | 使用 SQL 的 `JOIN`                   | 分開查詢，Python 中關聯結果          |
| 效能                  | 高效，但不適合關聯資料過多的情況      | 稍低，但適合處理大量關聯資料         |
| 使用場景              | 外鍵（`ForeignKey`）、一對一關聯      | 反向外鍵（`related_name`）、多對多關聯 |


根據資料關聯的類型選擇正確的方法，可以有效提升 Django 應用的效能

---

在某些情況下，兩者都可以使用，但選擇哪一個取決於以下因素：

1. **資料量大小**：
   - 如果關聯資料量較小，使用 **`select_related`** 更高效，因為只需要執行一次查詢。
   - 如果關聯資料量較大，使用 **`prefetch_related`** 更合適，因為它避免了 `JOIN` 導致的查詢結果過於龐大。

2. **關聯類型**：
   - **多對一或一對一**：優先使用 **`select_related`**。
   - **一對多或多對多**：優先使用 **`prefetch_related`**。

3. **查詢的靈活性**：
   - 如果需要對關聯表進行額外的過濾或排序，使用 **`prefetch_related`** 更靈活，因為它允許自訂查詢。
   - `select_related` 無法對關聯表進行過濾或排序，因為它直接使用 SQL 的 `JOIN`

> 當關聯表的資料量較大，且需要過濾或排序時，`prefetch_related` 是更好的選擇

---

## 3. **使用 Django Debug Toolbar**
[Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/) 是一個強大的工具，可以幫助開發者檢測 N+1 問題，並查看每個請求執行的 SQL 查詢。

### 安裝與設定：
1. 安裝：
   ```bash
   pip install django-debug-toolbar
   ```

2. 在 `settings.py` 中添加：
   ```python
   INSTALLED_APPS += ['debug_toolbar']
   MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
   INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
    ]
   ```

3. 在 `urls.py` 中添加：
   ```python
   from django.conf import settings
   from django.conf.urls import include
   from django.urls import path

   if settings.DEBUG:
       import debug_toolbar
       urlpatterns = [
           path('__debug__/', include(debug_toolbar.urls)),
       ] + urlpatterns
   ```

4. 啟動伺服器後，檢查每個請求的 SQL 查詢次數，找出 N+1 問題。

---

# 總結

- **N+1 問題** 是由於多次查詢資料庫導致的效能問題，特別是在處理關聯資料時容易發生。
- **解決方法**：
  1. 使用 `select_related` 解決一對一或多對一關聯的問題。
  2. 使用 `prefetch_related` 解決一對多或多對多關聯的問題。
  3. 使用 Django Debug Toolbar 檢測 SQL 查詢次數，找出潛在的 N+1 問題。
- **最佳實踐**：
  - 在開發過程中，定期檢查 SQL 查詢，確保效能最佳化。
  - 對於大型應用，考慮使用快取（如 Redis）進一步減少資料庫查詢次數。

透過這些方法，可以有效避免 N+1 問題，提升 Django 應用的效能與穩定性。