from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class bookinfo(models.Model):
    booktitle = models.CharField(default="", max_length=50)
    authorname = models.CharField(default="", max_length=50)
    bookdescription = models.TextField(default="", max_length=500)
    catagory = models.CharField(default="", max_length=50)
    language = models.CharField(default="", max_length=50)
    keyword = models.CharField(default="", max_length=50)
    bookcover = models.FileField(upload_to="bookcovers/")
    bookfile = models.FileField( upload_to="bookpdf/")
    uploadby = models.CharField(default="", max_length=50)
    
    def __str__(self):
        return self.booktitle
    
class booksdownloadrecord(models.Model):
    bookId = models.ForeignKey(bookinfo, on_delete=models.CASCADE)
    downloadby = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.bookId
        
    
