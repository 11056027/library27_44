from django.contrib import admin
from mysite.models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, CustomGroup

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author','chapter' ,'pub_date','place')

admin.site.register(Book, BookAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('name','email','password','password_confirm')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomGroup)