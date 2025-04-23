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