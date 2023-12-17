from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('',views.index, name="home"),
    path('all-books',views.all_books, name="all_books"),
    path('log-in',views.log_in, name="log_in"),
    path('authenticate-login', views.authenticate_login, name="authenticate_login"),
    path('authenticate-signin', views.authenticate_signin, name="authenticate_signin"),
    path('authenticate-logout', views.authenticate_logout, name="authenticate_logout"),
    path('upload-book', views.upload_book , name="upload_book"),
    path('all-books/detail<int:bookid>/', views.showdetailbook),
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)