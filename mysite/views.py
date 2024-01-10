from django.shortcuts import render
from django.shortcuts import redirect
from mysite.models import Book, CustomUser, CustomGroup
from datetime import datetime
from mysite.forms import UserRegisterForm,LoginForm
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def homepage(request):
    books = Book.objects.all()
    now = datetime.now()
    return render(request,'index.html',locals())

def showpost(request, slug):
    book=Book.objects.get(slug=slug)
    if book !=None:
        return render(request,'book.html',locals())
    else:
        return redirect("/")

def book_place(request, slug):
    book = Book.objects.get(slug=slug)
    return render(request, 'book.html', {'book': book})

def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        return render(request, 'register.html', locals())
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_email = form.cleaned_data['user_email']
            user_password = form.cleaned_data['user_password']
            user_password_confirm = form.cleaned_data['user_password_confirm']
            if user_password == user_password_confirm:
                user = User.objects.create_user(user_name, user_email, user_password)
                user.save()
                message = f'註冊成功！'
                return redirect('/login/')
            elif user_name == "":
                message = f'未輸入姓名'
                return render(request, 'register.html', locals())
            elif user_email == "":
                message = f'未輸入email'
                return render(request, 'register.html', locals())
            elif User.objects.filter(user_name=user_name).exists():
                message = "用戶名已存在。請選擇一個不同的用戶名。"
                return render(request, 'register.html', locals())
            else:
                message = f'兩次密碼不一致！'    
        return render(request, 'register.html', locals())
    else:
        message = "ERROR"
        return render(request, 'register.html', locals())

from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', locals())
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['user_name']
            user_password = form.cleaned_data['user_password']
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    message = '成功登入了'
                    return redirect('/')
                else:
                    message = '帳號尚未啟用'
            else:
                message = '登入失敗'

        return render(request, 'login.html', locals())
    else:
        message = "ERROR"
        return render(request, 'login.html', locals())