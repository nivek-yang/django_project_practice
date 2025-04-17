from django.forms import ModelForm
from .models import Interview

class InterviewForm(ModelForm):
    class Meta:
        model = Interview
        fields = ['comapany_name', 'position', 'interview_date', 'review', 'rating', 'result'] # 白名單
        


