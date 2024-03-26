from distutils.command.upload import upload
from email.policy import default
from sqlite3 import Timestamp
from turtle import mode
from django.db import models
from django.contrib.auth.models import User

class ProductDetail(models.Model):
    title = models.CharField(max_length= 200)
    description = models.TextField()
    # image = models.ImageField(upload_to='Donate/images/',blank = True,default = '')
    image = models.URLField(blank = True,default = '')
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    number = models.CharField(max_length=15,blank = True,)
    email = models.EmailField(blank = True,)
    contact_comments = models.TextField(blank = True,)
    category = models.CharField(max_length=30)
    sub_category = models.CharField(max_length=50,blank = True,)
    extra_comments = models.TextField(blank = True,)
    timeStamp = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    # userName = models.CharField(max_length=15)
    name = models.CharField(max_length=50,default='')

class MyChats(models.Model):
    initiatorId  = models.CharField(max_length= 30) 
    friendId = models.CharField(max_length= 30)
    initiatorName = models.CharField(max_length=200,)
    friendName = models.CharField(max_length= 200)
    lastMessage = models.TextField(blank=True)
    timeStampMessage = models.CharField(max_length= 300)
    timeStampChat = models.CharField(max_length= 300)


class FCMTokens(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    token = models.TextField()
    timestamp = models.CharField(max_length=50,blank=True)


class RequestedProductDetail(models.Model):
    title = models.TextField(blank=True)
    description = models.TextField()
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    number = models.CharField(max_length=15,blank = True,)
    email = models.EmailField(blank = True,)
    category = models.CharField(max_length=30,blank=True)
    sub_category = models.CharField(max_length=50,blank = True,)
    timeStamp = models.CharField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    # userId = models.IntegerField()
    # userName = models.CharField(max_length=15)
    name = models.CharField(max_length=50,blank=True)
