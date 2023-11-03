from django.shortcuts import render
from django.shortcuts import redirect
from mysite.models import Book
from datetime import datetime

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