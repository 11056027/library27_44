from django.shortcuts import render,redirect
from mysite.models import *
from datetime import *
from mysite.forms import *
from django.contrib import *
from django.shortcuts import *
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
#讀者註冊登入
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
                user = CustomUser.objects.create_user(user_name, user_email, user_password)
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
    
def managepage(request):
    return render(request, 'managepage.html' )

def readerpage(request):
    return render(request, 'readerpage.html')


def carlist(request, maker=0):
    car_maker = ['Ford', 'Honda', 'Mazda']
    car_list = [
        [{'model':'Fiesta', 'price': 203500},
            {'model':'Focus','price': 605000}, 
            {'model':'Mustang','price': 900000}],
		[{'model':'Fit', 'price': 450000}, 
		 {'model':'City', 'price': 150000}, 
		 {'model':'NSX', 'price':1200000}],
		[{'model':'Mazda3', 'price': 329999}, 
		 {'model':'Mazda5', 'price': 603000},
		 {'model':'Mazda6', 'price':850000}],]

    maker = maker
    maker_name =  car_maker[maker]
    cars = car_list[maker]
    return render(request, 'carlist.html', locals())
