from django.shortcuts import render,redirect,get_object_or_404
from mysite.models import *
from datetime import *
from mysite.forms import *
from django.contrib import *
from django.shortcuts import *
from django.contrib.auth import authenticate,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#基本
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
#讀者註冊登入登出
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
                user = CustomUser.objects.create_user(username=user_name, email=user_email, password=user_password)
                user.save()
                message = f'註冊成功！'
                return redirect('/login/')
            elif user_name == "":
                message = f'未輸入姓名'
                return render(request, 'register.html', locals())
            elif user_email == "":
                message = f'未輸入email'
                return render(request, 'register.html', locals())
            elif CustomUser.objects.filter(user_name=user_name).exists():
                message = "用戶名已存在。請選擇一個不同的用戶名。"
                return render(request, 'register.html', locals())
            else:
                message = f'兩次密碼不一致！'    
        return render(request, 'register.html', locals())
    else:
        message = "ERROR"
        return render(request, 'register.html', locals())

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
                    if user.is_staff:
                        # 如果是管理員，執行相應的操作
                        print("Admin logged in")
                        return redirect('/managepage/')
                    else:
                        # 如果是一般用戶，執行相應的操作
                        print("Regular user logged in")
                    auth.login(request, user)
                    print("success")
                    message = '成功登入了'
                    return redirect('/readerpage/')
                else:
                    message = '帳號尚未啟用'
            else:
                message = '登入失敗'

        return render(request, 'login.html', locals())
    else:
        message = "ERROR"
        return render(request, 'login.html', locals())
    
def logouts(request):
    logout(request)
    return redirect('/')
 
#書籍管理    
def book_place(request, slug):
    book = Book.objects.get(slug=slug)
    return render(request, 'book.html', {'book': book})

def book_list(request):
    books = Book.objects.all()
    return render(request, 'booklist.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('booklist')
    else:
        form = BookForm()
    return render(request, 'addbook.html', {'form': form})

def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    
    if request.method == 'POST':
        form = BookEditForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = BookEditForm(instance=book)
    
    return render(request, 'editbook.html', {'form': form, 'book': book})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    borrow_record = BorrowRecord.objects.filter(book=book).first() 
    return render(request, 'bookdetail.html', {'book': book, 'borrow_record': borrow_record})


def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)

    if book.place == '藏書中':
        # 更新書的狀態為外借中
        book.place = '外借中'
        book.save()

        # 創建借書記錄
        BorrowRecord.objects.create(book=book, borrower=request.user, borrow_date=timezone.now())

        return redirect('book_detail', book_id=book_id)
    else:
        # 書籍已經被借出
        return render(request, 'book_borrow_error.html', {'book': book})

def return_book(request, book_id):
    book = Book.objects.get(pk=book_id)

    if book.place == '外借中':
        # 更新書的狀態為藏書中
        book.place = '藏書中'
        book.save()

        # 找到借書記錄，並更新還書日期
        borrow_record = BorrowRecord.objects.get(book=book, borrower=request.user, return_date__isnull=True)
        borrow_record.return_date = timezone.now()
        borrow_record.save()

        return redirect('book_detail', book_id=book_id)
    else:
        # 書籍不在外借中
        return render(request, 'book_return_error.html', {'book': book})
    
def toborrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.is_borrowed:
        messages.error(request, '該書籍已經被借出。')
    else:
        book.is_borrowed = True
        book.borrower = request.user
        book.save()
        messages.success(request, f'成功借出書籍：{book.title}。')

    return redirect('book_detail', slug=book.slug)

def toreturn_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if not book.is_borrowed:
        messages.error(request, '該書籍尚未被借出。')
    elif book.borrower != request.user:
        messages.error(request, '你不能歸還這本書，因為你不是借閱者。')
    else:
        book.is_borrowed = False
        book.borrower = None
        book.save()
        messages.success(request, f'成功歸還書籍：{book.title}。')

    return redirect('book_detail', slug=book.slug)
    
def managepage(request):
    return render(request, 'managepage.html' )

def readerpage(request):
    return render(request, 'readerpage.html')

