from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import *
from products import views

router = DefaultRouter()
router.register(r'my-product', views.MyProducts, basename='my-product')
router.register(r'all', views.Products, basename='product'),

urlpatterns = [
    path('add/', AddProductView.as_view(), name='add-product'),
    path('update/<int:pk>/',
         UpdateProduct.as_view(), name='update-product'),

    path('delete/', DeleteProduct.as_view(), name='delete-product'),
    path('', include(router.urls))
]
