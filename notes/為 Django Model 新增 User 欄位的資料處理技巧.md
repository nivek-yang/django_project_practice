---
title: 為 Django Models 新增 User 欄位的資料處理技巧
date: 2025-04-23
categories:
  - [技術筆記]
tags:
  - Python
  - Django
  - Database
---

在 Django 開發中，當我們需要為現有的模型新增欄位時，特別是與其他模型的關聯欄位，可能會遇到一些資料處理上的挑戰。本文將以為 `Interview` 模型新增 `user` 欄位為例，說明如何處理資料庫遷移、預設值設定，以及表單資料的處理方式。

---

# 為 Interview 模型新增 User 欄位

在 `Interview` 模型中新增一個與 `User` 模型的關聯欄位：

```python
user = models.ForeignKey(User, on_delete=models.CASCADE)
```

這樣的設計表示每個 `Interview` 都必須關聯到一個 `User`，且當該 `User` 被刪除時，相關的 `Interview` 也會被刪除 (`on_delete=models.CASCADE`)。

---

## makemigrations 時的問題與解決方法

當我們執行 `makemigrations` 時，如果新增的欄位沒有設定 `null=True`，Django 會要求我們為現有的資料設定預設值。這是因為資料庫中已經存在的 `Interview` 資料並沒有 `user_id` 欄位，而該欄位又不允許為空。

### 解決方法

1. **建立一個「匿名使用者」帳號**  
   我們可以先註冊一個使用者，並將其名稱設為「匿名使用者」。這樣，所有原本的 `Interview` 資料都可以關聯到這個使用者。

2. **在 `makemigrations` 時設定預設值**  
   當執行 `makemigrations` 時，Django 會提示以下選項：

   ```
   1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
   ```

   選擇 `1`，並輸入 `1` 作為預設值，表示將所有現有的 `Interview` 資料的 `user_id` 設定為 ID 為 1 的使用者（即「匿名使用者」）。

   ```plaintext
   Select an option: 1
   Please enter the default value as valid Python.
   >>> 1
   ```

3. **執行資料庫遷移**  
   接著執行 `migrate`，更新資料庫結構。這樣，`Interview` 資料表中會新增 `user_id` 欄位，且所有現有資料的 `user_id` 預設為 1。

---

# 建立 Interview 資料的方式

在新增 `user` 欄位後，我們需要在建立 `Interview` 資料時，確保正確地關聯到當前登入的使用者 (`req.user`)。以下是兩種常見的處理方式：

## 作法一：使用 `form.save(commit=False)`

這是 Django 中處理表單資料的標準方式之一：

```python
form = InterviewForm(req.POST)
interview = form.save(commit=False)  # 先將資料準備好，但不存入資料庫
interview.user = req.user  # 將當前登入的使用者關聯到 Interview
interview.save()  # 最後存入資料庫
```

這種方式的優點是可以在儲存資料前，對資料進行額外的處理，例如設定關聯欄位。

---

## 作法二：嘗試字典合併（不可行）

另一種看似可行的方式是將 `req.POST` 與其他資料合併成一個字典，然後直接傳入表單。但需要注意的是，`req.POST` 並不是真正的字典，因此這種方法不可行。

Django 的 `QueryDict`（如 req.POST）的值是列表，即使只有一個值。例如：

```python
req.POST = {"name": ["John"], "age": ["30"]}
```

即使將 req.POST 轉成 python 字典，仍要再將資料轉換型態，因此選用作法一比較適合

### 字典合併範例

```python
a = {'a': 1}
b = {'b': 2}

# 字典合併的兩種方式
c = a | b  # Python 3.9+
c = {**a, **b}  # Python 3.5+
```

### 嘗試將 `req.POST` 與其他資料合併

```python
form = InterviewForm(req.POST | {"user": req.user})  # 看似可行，但實際上不行
```

由於 `req.POST` 是 `QueryDict` 類型，而不是標準的 Python 字典，因此無法直接使用字典合併的方式處理。

---

# 結論

在 Django 中，為模型新增欄位時需要特別注意資料庫遷移的處理，尤其是當欄位不允許為空時。我們可以透過建立「匿名使用者」帳號並設定預設值來解決這個問題。

在處理表單資料時，建議使用 `form.save(commit=False)` 的方式，這樣可以靈活地對資料進行額外處理，例如設定關聯欄位。

希望本文能幫助你更好地理解 Django 中模型欄位新增與表單資料處理的技巧！