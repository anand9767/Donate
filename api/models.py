from distutils.command.upload import upload
from django.db import models

class ProductDetail(models.Model):
    title = models.CharField(max_length= 200)
    description = models.TextField()
    image = models.ImageField(upload_to='Donate/images/')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    contact_comments = models.TextField()
    category = models.CharField(max_length=30)
    sub_category = models.CharField(max_length=50)
    extra_comments = models.TextField()
    userId = models.IntegerField()
    userName = models.CharField(max_length=15)
    name = models.CharField(max_length=50,default='')