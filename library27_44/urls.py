"""
URL configuration for library27_44 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from mysite.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('book/<slug:slug>/', showpost),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logouts, name='logouts'),

    path('booklist/', book_list, name='booklist'),
    path('addbook/', add_book, name='addbook'),
    path('bookdetail/<int:book_id>/', book_detail, name='book_detail'),
    path('editbook/<int:book_id>/', edit_book, name='editbook'),
    path('',homepage, name='homepage'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('return/<int:book_id>/', return_book, name='return_book'),
    path('managepage/', managepage, name='managepage'),
    path('readerpage/', readerpage, name='readerpage'),
    path('toborrow/', toborrow_book, name='toborrow_book'),
    path('toreturn/', toreturn_book, name='toreturn_book'),
]
