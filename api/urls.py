from ast import Delete
from email.mime import base
from posixpath import basename
from tkinter import N
from unicodedata import name
from .views import CreateOrUpdateFCMToken, RegisterAPI,LoginAPI,ChangePasswordView,CustomAuthToken, UpdateProduct, UpdateUser
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('api/user',views.UserList,basename = 'user')
router.register('api/myproduct',views.MyProducts,basename = 'myproduct')
router.register('api/product',views.Products,basename = 'product'),
router.register('api/mychats',views.Chats,basename='mychats'),
router.register('api/getTokens',views.GetFCMToken,basename='mytokens'),

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/',LoginAPI.as_view(),name='login'),
    path('api/deleteproduct/',views.delete_product,name='deleteproduct'),
    path('api/deleteuser/',views.delete_user,name='deleteuser'),
    path('api/updateproduct/',UpdateProduct.as_view(),name='updateproduct'),
    path('api/updateuser/',UpdateUser.as_view(),name='updateuser'),
    path('api/resetpassword/',ChangePasswordView.as_view(),name='changepassword'),
    path('api/token/auth/', CustomAuthToken.as_view()),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/updateFCMToken/',csrf_exempt(CreateOrUpdateFCMToken.as_view()),name='updateFCMToken'),
    path('',include(router.urls))
]