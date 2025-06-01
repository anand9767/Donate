from django.db import models
from api.models import *

# Create your models here.


# class ProductDetail(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     # image = models.ImageField(upload_to='Donate/images/',blank = True,default = '')
#     image = models.URLField(blank=True, default='')
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     number = models.CharField(max_length=15, blank=True,)
#     email = models.EmailField(blank=True,)
#     contact_comments = models.TextField(blank=True,)
#     category = models.CharField(max_length=30)
#     sub_category = models.CharField(max_length=50, blank=True,)
#     extra_comments = models.TextField(blank=True,)
#     timeStamp = models.DateTimeField(max_length=50)
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE,)
#     # userName = models.CharField(max_length=15)
#     name = models.CharField(max_length=50, default='')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class ProductImage(models.Model):
    product = models.ForeignKey(
        ProductDetail, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

