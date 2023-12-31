from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import get_object_or_404
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models.functions import Random
import os
from django.conf import settings
import mimetypes

# Create your views here.

def index(request):
    param = {
            'data': bookinfo.objects.all()[:3]
        }
    return render(request,"index.html",param)

def all_books(request):
    cnt = 0
    data = None  # Initialize data to None

    if request.method == "GET":
        form_val = request.GET.get("search")
        if form_val is not None:
            data = bookinfo.objects.filter(booktitle__icontains=form_val)
        else:
            data = bookinfo.objects.filter(status = "on").order_by('?')  # '?' for random ordering
        cnt = len(data)

    param = {
        'data': data,
        'length': cnt
    }
    return render(request, "allbooks.html", param)

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
            bookfile = bookpdf,
            uploadby = request.user.username).save()
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

def downloadbook(request,bookid):
    book_instance = bookinfo.objects.get(id=bookid)
    if not totaldownloaders.objects.filter(bookid=book_instance, downloade_by=request.user.username).exists():
        totaldownloaders.objects.create(bookid=book_instance, downloade_by=request.user.username)

    data = bookinfo.objects.get(id=bookid)
    file_path = os.path.join(settings.MEDIA_ROOT, str(data.bookfile))
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=mimetypes.guess_type(file_path)[0])
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response

def profile(request):
    print(request.user.username)
    return redirect("upload_book")

def manage_book(request):
    if request.method == "POST":
        booktitle = request.POST.get("booktitle")
        authorname = request.POST.get("authorname")
        language = request.POST.get("language")
        status = request.POST.get("active")
        id = request.POST.get("id")
        info = bookinfo.objects.get(id = id)
        info.booktitle = booktitle 
        info.authorname = authorname 
        info.language = language 
        info.status = status 
        info.save()

    if request.method == "GET":
        id = request.GET.get("id")
        if id == None:
            pass
        else:
            try:
                info = get_object_or_404(bookinfo, id=id)
                info.delete()
                return redirect("profile")
            except bookinfo.DoesNotExist:
                print("Book not found")
    download_list = []
    data = bookinfo.objects.filter(uploadby = request.user.username)
    if data is not None:
        for i in data:
            download_list.append(totaldownloaders.objects.filter(bookid = i.id).count())

    param = {
        'data' : zip(data,download_list)
    }
    return render(request, "manage-book.html", param)