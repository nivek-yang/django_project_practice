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




