from django.db import models
from django.contrib.auth.models import User

class Interview(models.Model):
    company_name = models.CharField(max_length=100, help_text="至少需要 3 個字")
    position = models.CharField(max_length=50)
    interview_date = models.DateField(null=True)
    review = models.TextField() # 專門拿來放很多字的欄位
    rating = models.PositiveSmallIntegerField(
        help_text="1 ~ 10 分，1 分最低，10 分最高"
    )
    result = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorited_by = models.ManyToManyField(
        User,
        through="FavoriteInterview",
        related_name="favorite_interview", # join 欄位
    )

# - Table
#     - 公司名稱 company_name
#     - 職位 position
#     - 面試日期 interview_date
#     - 心得 review
#     - 評分 rating

class Comment(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)
    # 有幾種 on_delete 的方法：models.CASCADE, models.DO_NOTHING, models.RESTRICT, models.SET_NULL
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# join table
class FavoriteInterview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE)