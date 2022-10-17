from django.contrib import admin
from .models import MenuItem,Item
# Register your models here.

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','type','quantity']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id','name','image','menuItem','description','ingredients','nutritionalValue']