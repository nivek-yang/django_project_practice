from django.contrib import admin
from .models import Interview

# 能客製化後台管理系統的類別，非必要
class InterviewAdmin(admin.ModelAdmin):
    pass

# 註冊
admin.site.register(Interview, InterviewAdmin)