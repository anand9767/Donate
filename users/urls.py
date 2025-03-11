from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserList, basename='user')

urlpatterns = [
    path('register/', views.RegisterAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('update/', views.UpdateUser.as_view(), name='update-user'),
    path('delete/', views.delete_user, name='deleteuser'),
    # path('reset-password/', views.ChangePasswordView.as_view(),
    #      name='changepassword'),
    path('delete-account-request/', views.DeleteAccountRequestViewSet.as_view(
        {'post': 'create'}), name='delete-account-request'),
]
