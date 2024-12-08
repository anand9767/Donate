from django.shortcuts import render

from firebase_admin import messaging


def send_fcm_notification(token, title, body, data=None):
    """
    Send a push notification using Firebase Cloud Messaging.
    
    Args:
        token (str): The FCM device token.
        title (str): Notification title.
        body (str): Notification body.
        data (dict): Optional custom data payload.
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
        data=data or {},  # Optional custom data payload
    )
    try:
        response = messaging.send(message)
        return response
    except Exception as e:
        print(f"Error sending notification: {e}")
        return None
