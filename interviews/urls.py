from django.urls import path
from . import views

app_name = "interviews"

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("<int:id>", views.show, name="show"), # id 變數會被當作關鍵字引數傳到 show()
    path("<int:id>/edit", views.edit, name="edit")
]