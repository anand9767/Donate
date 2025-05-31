from rest_framework.views import APIView
from rest_framework.response import Response
# Require authentication if needed
# Assuming the function is in utils.py
from .utils import send_fcm_notification
from rest_framework import generics, status, authentication, permissions
from rest_framework.response import Response
from api.models import FCMTokens
from api.serializers import MyFCMTokenSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class SendNotificationView(APIView):
    def post(self, request):
        token = request.data.get(
            'fcm_token')
        title = request.data.get('title')
        body = request.data.get('body')

        # Send notification to all tokens of the recipient
        result = send_fcm_notification(token, title, body)

        return Response({
            "message": "Notification sent successfully.",
        })
    

class SendNotificationViewNew(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        title = request.data.get('title')
        body = request.data.get('body')

        if not user_id or not title or not body:
            return Response({
                "success": False,
                "message": "user_id, title, and body are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        # Get all FCM tokens for the user
        tokens = FCMTokens.objects.filter(
            user=user).values_list('token', flat=True)

        if not tokens:
            return Response({
                "success": False,
                "message": "No FCM tokens found for the user."
            }, status=status.HTTP_404_NOT_FOUND)

        # Send notification to all tokens
        for token in tokens:
            send_fcm_notification(token, title, body)

        return Response({
            "success": True,
            "message": "Notification sent successfully.",
            "sent_to": list(tokens)
        }, status=status.HTTP_200_OK)
    

class CreateFCMToken(generics.CreateAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = FCMTokens.objects.all()
    serializer_class = MyFCMTokenSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        token = request.data.get('token')
        existing = FCMTokens.objects.filter(token=token).first()
        if existing:
            return Response({
                "success": False,
                "message": "Token already exists",
                "data": MyFCMTokenSerializer(existing).data
            }, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data={
            "user": request.user.id,
            "token": token
        })

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Token saved successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Failed to save token.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
