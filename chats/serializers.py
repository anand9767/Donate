from rest_framework import serializers
from .models import MyChats


class ChatListSerializer(serializers.ModelSerializer):
    initiator_name = serializers.SerializerMethodField()
    friend_name = serializers.SerializerMethodField()

    class Meta:
        model = MyChats
        fields = [
            'initiator',
            'friend',
            'chat_room_id',
            'sender',
            'timeStampMessage',
            'initiator_name',
            'friend_name',
        ]

    def get_initiator_name(self, obj):
        return f"{obj.initiator.first_name} {obj.initiator.last_name}".strip()

    def get_friend_name(self, obj):
        return f"{obj.friend.first_name} {obj.friend.last_name}".strip()

    def validate(self, data):
        if MyChats.objects.filter(chat_room_id=data.get('chat_room_id')).exists():
            raise serializers.ValidationError("Chat room already exists.")
        return data


class ChatCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyChats
        fields = ['initiator', 'friend', 'chat_room_id',
                  'sender', 'timeStampMessage']

    def validate(self, data):
        # Prevent duplicate chat room creation
        if MyChats.objects.filter(chat_room_id=data.get('chat_room_id')).exists():
            raise serializers.ValidationError("Chat room already exists.")
        return data
