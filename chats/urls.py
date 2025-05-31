from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import *

router = DefaultRouter()

urlpatterns = [
    path('list/', UserChatList.as_view(), name='user-chat-list'),
    path('create/', CreateChatRoom.as_view(), name='create-chat-room'),

    path('', include(router.urls))
]
