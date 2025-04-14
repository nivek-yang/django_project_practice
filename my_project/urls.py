from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("myapp.urls")),
    path("myapp2/", include("myapp2.urls")),
    path("interviews/", include("interviews.urls")),
]
