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
    latitude = models.FloatField()
    longitude = models.FloatField()
    number = models.CharField(max_length=15,blank = True,)
    email = models.EmailField(blank = True,)
    contact_comments = models.TextField(blank = True,)
    category = models.CharField(max_length=30)
    sub_category = models.CharField(max_length=50,blank = True,)
    extra_comments = models.TextField(blank = True,)
    timeStamp = models.DateTimeField(max_length=50)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,)
    # userName = models.CharField(max_length=15)
    name = models.CharField(max_length=50,default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MyChats(models.Model):
    initiatorId  = models.CharField(max_length= 30) 
    friendId = models.CharField(max_length= 30)
    initiatorName = models.CharField(max_length=200,)
    friendName = models.CharField(max_length= 200)
    lastMessage = models.TextField(blank=True)
    chat_room_id = models.TextField(max_length=50, null=True, blank=True)
    sender = models.IntegerField(null=True, blank=True)
    timeStampMessage = models.CharField(max_length= 300)
    timeStampChat = models.CharField(max_length= 300)


class FCMTokens(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    token = models.TextField()
    timestamp = models.DateTimeField()


class RequestedProductDetail(models.Model):
    title = models.TextField(blank=True)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    number = models.CharField(max_length=15,blank = True,)
    email = models.EmailField(blank = True,)
    category = models.CharField(max_length=30,blank=True)
    sub_category = models.CharField(max_length=50,blank = True,)
    timeStamp = models.DateTimeField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    # userId = models.IntegerField()
    # userName = models.CharField(max_length=15)
    name = models.CharField(max_length=50,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class DeleteAccountRequest(models.Model):
#     reasonForDelete = models.TextField()
#     requestStatus = models.BooleanField(default=False)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
