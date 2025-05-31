from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import MyChats
from .serializers import *
from django.db import models


class UserChatList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            chats = MyChats.objects.filter(
                models.Q(initiator=user) | models.Q(friend=user)
            ).order_by('-timeStampChat')

            serializer = ChatListSerializer(chats, many=True)
            return Response({
                "success": True,
                "message": "Chat list fetched successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to fetch chat list",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        

class CreateChatRoom(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChatCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Chat room created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Failed to create chat room.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
