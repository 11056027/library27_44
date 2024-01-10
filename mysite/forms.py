from django import forms
from mysite import models
from .models import Book

class UserRegisterForm(forms.Form):
    user_name = forms.CharField(label='您的帳號', max_length=50)
    user_email = forms.EmailField(label='電子郵件')
    user_password = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)
    user_password_confirm = forms.CharField(label='輸入確認密碼', widget=forms.PasswordInput)
    is_staff = forms.BooleanField(label='是否為管理員', required=False)  # 新增的 is_staff 字段

    def clean(self):
        cleaned_data = super().clean()
        user_password = cleaned_data.get('user_password')
        user_password_confirm = cleaned_data.get('user_password_confirm')

        # 檢查密碼一致性
        if user_password and user_password_confirm and user_password != user_password_confirm:
            raise forms.ValidationError("兩次密碼不一致")

        return cleaned_data

class LoginForm(forms.Form):
    user_name = forms.CharField(label='您的帳號', max_length=50, initial='leonlin')
    user_password = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)
    
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'slug','author','pub_date','content','imgcode', 'place']

class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'chapter', 'content', 'imgcode','place']


    

