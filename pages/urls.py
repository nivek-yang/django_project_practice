from django.urls import path
from . import views

app_name="pages"

urlpatterns = [
    path("", views.index, name = "index"),
    path("about", views.about, name = "about"),
    path("contact", views.contact, name = "contact"),
    path("payment", views.payment, name = "payment"),
    path("paid", views.paid, name = "paid")
]