from django.forms import ModelForm
from .models import Interview

# Create the form class
class InterviewForm(ModelForm):
    class Meta:
        model = Interview
        
        # 有些欄位不想被寫入
        # exclude = ['is_admin']

        # 接受所有欄位，不建議
        # fields = "__all__"

        # 設置白名單
        fields = ['company_name', 'position', 'interview_date', 'review', 'rating', 'result'] 
        labels = {'company_name': "公司名稱",
                  'position': "職位",
                  'interview_date': "面試日期",
                  'review': "心得",
                  'rating': "評分",
                  'result': "面試結果"}
        help_texts = {'company_name': "至少需要 3 個字",
                      'rating': "1 ~ 10 分，1 分最低，10 分最高"}
        




