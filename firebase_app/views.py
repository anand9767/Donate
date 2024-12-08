from rest_framework.views import APIView
from rest_framework.response import Response
# Require authentication if needed
# Assuming the function is in utils.py
from .utils import send_fcm_notification


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
