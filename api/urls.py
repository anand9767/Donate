from ast import Delete
from email.mime import base
from posixpath import basename
from tkinter import N
from unicodedata import name
from .views import *
from django.urls import path,include
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('api/user',views.UserList,basename = 'user')
router.register('api/my-product',views.MyProducts,basename = 'my-product')
router.register('api/product',views.Products,basename = 'product'),
router.register('api/my-requested-product',views.MyRequestedProducts,basename = 'my-requested-product')
router.register('api/requested-products',views.RequestedProducts,basename = 'requested-products'),
router.register('api/my-chats',views.Chats,basename='my-chats'),
router.register('api/getTokens',views.GetFCMToken,basename='getTokens'),
router.register('api/delete-account-request',
                views.DeleteAccountRequestViewSet, basename='delete-account-request'),

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    # path('api/delete-account-request', DeleteAccountRequest.as_view(), name='delete-account-request'),
    path('api/login/',LoginAPI.as_view(),name='login'),
    path('api/deleteproduct/',views.delete_product,name='deleteproduct'),
    path('api/deleterequestedproduct/',views.delete_requested_product,name='deleterequestedproduct'),
    path('api/deleteuser/',views.delete_user,name='deleteuser'),
    path('api/updateproduct/',UpdateProduct.as_view(),name='updateproduct'),
    path('api/updateuser/',UpdateUser.as_view(),name='updateuser'),
    path('api/resetpassword/',ChangePasswordView.as_view(),name='changepassword'),
    path('api/token/auth/', CustomAuthToken.as_view()),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/updateFCMToken/',csrf_exempt(CreateOrUpdateFCMToken.as_view()),name='updateFCMToken'),
    path('',include(router.urls))
]