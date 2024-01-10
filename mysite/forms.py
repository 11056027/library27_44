from django import forms
from mysite import models
from .models import Book

class UserRegisterForm(forms.Form):
    user_name = forms.CharField(label='您的帳號', max_length=50)
    user_email = forms.EmailField(label='電子郵件')
    user_password = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)
    user_password_confirm = forms.CharField(label='輸入確認密碼', widget=forms.PasswordInput)
    
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

