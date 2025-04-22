from django.forms import ModelForm
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]
        labels = {
            'username': "帳號",
            'password': "密碼",
            'email': "信箱",
            'first_name': "名",
            'last_name': "姓",            
        }