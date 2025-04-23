SPA = single page application 把內容、url 抽換掉 路徑是假的
SSR = server side render

html -> form -> submit -> django 收 -> req.POST[""]
                                    -> model_form
     home  <--- redirect <----

// 打 api
// 前後端分離
js -> submit -> 
            json <---
            createElement
            DOM

<a>: GET
<form>: GET/POST

logout:
     delete /sessions (理論上)
     post users/logout (html 只能用 get/post)

**QueryString**  /?a=1&b=2 當作網址參數


---
localhost/?a=1&b=2&c=3

Python (在 django template 不能用):
     request.GET['c'] => 3

     def index(req):
          a = req.GET['a']
          b = req.GET['b']
          c = req.GET['c']

          return render(req, "pages/index.html, {"a": a, "b": b, "c": c})

HTML:
     <QueryDict>

---

登入 -> 憑證
操作 CRUD -> 授權

---
為 Interview model 建立 user 欄位

user = models.ForeignKey(User, on_delete=models.CASCADE)

makemigrations 在新增欄位時如果沒設定 null=True 會遇到要設定預設值的問題
假如多增加 user_id 欄位，原本建立的 interview 資料 沒有 user_id，
但是 user_id 欄位 不應該是 null
解決方法： 可以掛人頭帳號，先註冊一個使用者，把他的名字設為 "匿名使用者" ，以前的 interview 都是該使用者的

在 makemigrations 時用 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)

Select an option: 1
Please enter the default value as valid Python.
輸入 1 ， 代表將 user_id 設定為 1

再用 migrate 更新資料庫
這樣原本 interview 資料表裡會多出 user_id 欄位，值為 1
