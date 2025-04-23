from django.urls import path
from . import views

app_name="users"

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("login", views.create_session, name="create_session"),  # 需要用到內部函數 login，所以取名 create_session
    path("logout", views.delete_session, name="logout"), # 需要用到內部函數 logout，所以取名 delete_session
]
