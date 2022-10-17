from ast import Delete
from email.mime import base
from posixpath import basename
from tkinter import N
from unicodedata import name
from .views import MenuItemViewSet
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.routers import DefaultRouter

from webApi import views

router = DefaultRouter()

router.register('menuitem',views.MenuItemViewSet,basename = 'menuitem')
router.register('item',views.ItemViewSet,basename = 'item')



urlpatterns = [
    path('webapi/',include(router.urls))
]