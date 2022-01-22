from email.mime import base
from posixpath import basename
from .views import RegisterAPI,LoginAPI, UserList
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('api/user',views.UserList,basename = 'user')
router.register('api/myproduct',views.MyProducts,basename = 'myproduct')
router.register('api/product',views.Products,basename = 'product')

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/',LoginAPI.as_view(),name='Login'),
    path('api/deleteproduct/',views.delete_Product),
    path('api/deleteuser/',views.delete_User),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('',include(router.urls))
]