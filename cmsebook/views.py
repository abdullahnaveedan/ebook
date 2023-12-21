from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .models import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models.functions import Random
# Create your views here.

def index(request):
    param = {
            'data': bookinfo.objects.all()[:3]
        }
    return render(request,"index.html",param)

def all_books(request):
    data = bookinfo.objects.all().order_by(Random())
    param = {'data' : data}
    return render(request, "allbooks.html",param)

def log_in(request):
    return render(request, "login.html")

def authenticate_signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("confirmPassword")
        user = User.objects.create_user(username = username , email = email, password = password)
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
    return redirect("log_in")

def authenticate_login(request): 
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request,username = username,password = password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
    return redirect("log_in")

def authenticate_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect("home")

def upload_book(request):
    if request.method == "POST":
        booktitle = request.POST.get("booktitle")
        authorname = request.POST.get("authorname")
        bookdescription = request.POST.get("bookdescription")
        catagory = request.POST.get("catagory")
        language = request.POST.get("language")
        keyword = request.POST.get("keyword")
        bookcover = request.FILES.get('bookcover', None)
        bookfile = request.FILES.get('bookpdf', None)
        bookcoverimage = ''

        if bookcover:
            file_name = default_storage.save('bookcovers/' + bookcover.name, ContentFile(bookcover.read()))
            bookcoverimage = file_name
        else:
            bookcoverimage = ''

        bookpdf = ''
        if bookfile:
            file_name = default_storage.save('bookpdf/' + bookfile.name, ContentFile(bookfile.read()))
            bookpdf = file_name
        else:
            bookpdf = ''


        bookinfo(
            booktitle = booktitle,
            authorname = authorname,
            bookdescription = bookdescription,
            catagory = catagory,
            language = language,
            keyword = keyword,
            bookcover = bookcoverimage,
            bookfile = bookpdf).save()
        return redirect("all_books")
    return render(request, "uploadbook.html")

def showdetailbook(request, bookid):
    if request.user.is_authenticated:
        param = {
            'data': bookinfo.objects.get(id=bookid)
        }
        return render(request, "bookdetail.html", param)
    return redirect("log_in")

def top_trend(request):
    param = {
            'data': bookinfo.objects.all()[:3]
    }
    return render(request,"top_trend.html",param)