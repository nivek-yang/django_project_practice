from django.forms import ModelForm, DateInput
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
        # 改變欄位名稱
        labels = {'company_name': "公司名稱",
                  'position': "職位",
                  'interview_date': "面試日期",
                  'review': "心得",
                  'rating': "評分",
                  'result': "面試結果"}
        # 控制欄位的 type，沒有的話 form 會自己猜是什麼 type
        widgets = {'interview_date': DateInput({"type": "date"})} 
        




