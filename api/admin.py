from django.contrib import admin
from .models import ProductDetail
# Register your models here.

@admin.register(ProductDetail)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','image','latitude','longitude','number','email','contact_comments','category','sub_category','extra_comments','userId','userName']
