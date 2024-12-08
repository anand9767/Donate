from django.urls import path
from .views import SendNotificationView

urlpatterns = [
    path('api/send-notification/', SendNotificationView.as_view(),
         name='send-notification'),
]
