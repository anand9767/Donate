# models.py

from django.db import models
from django.contrib.auth.models import User


class DonationStory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    story_text = models.TextField()
    image = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
