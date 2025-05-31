# serializers.py

from rest_framework import serializers
from .models import DonationStory


class DonationStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationStory
        fields = ['id','user' ,'title', 'story_text',
                  'image', 'created_at', 'is_approved']
        read_only_fields = ['id', 'created_at', 'is_approved']
