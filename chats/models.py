from django.db import models
from django.contrib.auth.models import User  # type: ignore
# Create your models here.


class MyChats(models.Model):
    initiator = models.ForeignKey(
        User, related_name='initiated_chats', on_delete=models.CASCADE)
    friend = models.ForeignKey(
        User, related_name='received_chats', on_delete=models.CASCADE)
    chat_room_id = models.CharField(
        max_length=50, null=True, blank=True, unique=True)
    sender = models.ForeignKey(
        User, related_name='last_sent_chats', null=True, blank=True, on_delete=models.SET_NULL)
    timeStampMessage = models.DateTimeField(null=True, blank=True)
    timeStampChat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.initiator.username} ↔ {self.friend.username}"
