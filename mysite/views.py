from django.shortcuts import render
from django.shortcuts import redirect
from mysite.models import Book
from datetime import datetime

# Create your views here.
def homepage(request):
    posts = Book.objects.all()
    now = datetime.now()
    return render(request,'index.html',locals())

def showpost(request,slug):
    post=Book.objects.get(slug=slug)
    if post !=None:
        return render(request,'post.html',locals())
    else:
        return redirect("/")