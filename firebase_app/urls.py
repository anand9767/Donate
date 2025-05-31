from django.urls import path
from .views import *

urlpatterns = [
    path('api/send-notification/', SendNotificationView.as_view(),
         name='send-notification'),
    path('api/v2/create-fcm-token/', CreateFCMToken.as_view(),
         name='create-fcm-token'),
    path('api/v2/send-notification/', SendNotificationViewNew.as_view(),
         name='send-notification'),
]
