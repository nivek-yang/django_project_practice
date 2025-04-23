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