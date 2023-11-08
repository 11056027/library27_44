from django.contrib import admin
from mysite.models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug','author','chapter' ,'pub_date','place')

admin.site.register(Book, BookAdmin)