from django.db import models

class Interview(models.Model):
    company_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    interview_date = models.DateField(null=True)
    review = models.TextField() # 專門拿來放很多字的欄位
    rating = models.PositiveSmallIntegerField()
    result = models.CharField(max_length=100, null=True)

# - Table
#     - 公司名稱 company_name
#     - 職位 position
#     - 面試日期 interview_date
#     - 心得 review
#     - 評分 rating