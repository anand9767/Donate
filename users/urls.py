from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserList, basename='user')

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('update/<int:pk>/', views.UpdateUser.as_view(), name='user-update'),
    path('delete/', views.DeleteUser.as_view(), name='delete-user'),
    # path('reset-password/', views.ChangePasswordView.as_view(),
    #      name='changepassword'),
    path('delete-account-request/', views.DeleteAccountRequestViewSet.as_view(
        {'post': 'create'}), name='delete-account-request'),
    path('', include(router.urls))
]
