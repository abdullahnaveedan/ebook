from django.db import models

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
    def __str__(self):
        return self.booktitle
    