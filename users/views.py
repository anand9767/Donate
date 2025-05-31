from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User
from rest_framework import status, permissions, authentication
from rest_framework.views import APIView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import UserSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import login
from knox.auth import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils.decorators import method_decorator
from rest_framework import status, generics, authentication, permissions  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework.decorators import api_view, authentication_classes, permission_classes # type: ignore
from django.http import JsonResponse # type: ignore
from django.contrib.auth import login # type: ignore
from django.views.decorators.csrf import csrf_exempt # type: ignore
from knox.views import LoginView as KnoxLoginView # type: ignore
from knox.auth import AuthToken # type: ignore
from rest_framework.authtoken.serializers import AuthTokenSerializer # type: ignore
from django.contrib.auth.models import User # type: ignore
import io
from rest_framework import viewsets # type: ignore
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from .models import *
from .serializers import *
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator 
import logging
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)  # Setup logging

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "status": "success",
                "message": "User Registered Successfully",
                "data": {
                    "user": serializer.data,
                    "token": AuthToken.objects.create(user)[1]
                }
            }, status=status.HTTP_201_CREATED)

        # Extract a single message for simplicity
        error_messages = []
        for field, messages in serializer.errors.items():
            # Take the first error message
            error_messages.append(f"{messages[0]}")

        return Response({
            "status": "error",
            "message": error_messages[0] if error_messages else "Registration failed"
        }, status=status.HTTP_400_BAD_REQUEST)


# Ensure CSRF is fully disabled
# Ensure CSRF is fully disabled
@method_decorator(csrf_exempt, name='dispatch')
class LoginAPI(KnoxLoginView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)

        if not serializer.is_valid():  # Handle validation errors separately
            errors = serializer.errors  # Get error dictionary

            # Check if it's an authentication issue
            if "non_field_errors" in errors:
                return Response({
                    "status": "error",
                    # Extract first meaningful error
                    "message": errors["non_field_errors"][0]
                }, status=status.HTTP_400_BAD_REQUEST)

            # General validation error (e.g., missing fields)
            error_message = list(errors.values())[
                0][0] if errors else "Invalid credentials"
            return Response({
                "status": "error",
                "message": error_message
            }, status=status.HTTP_400_BAD_REQUEST)

        # If credentials are valid, log the user in
        user = serializer.validated_data['user']
        login(request, user)
        response = super().post(request, format=None)
        user_data = UserSerializer(user).data

        return Response({
            "status": "success",
            "message": "User logged in successfully",
            "data": {
                "user": user_data,
                "token": response.data["token"]
            }
        }, status=status.HTTP_200_OK)


class UpdateUser(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'pk'  # optional, this is the default

    def put(self, request, *args, **kwargs):
        try:
            user = self.get_object()  # this now uses pk from the URL
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "User updated successfully",
                    "user": serializer.data
                }, status=status.HTTP_200_OK)
            return Response({
                "message": "Update failed",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                "message": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "message": "An unexpected error occurred",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteUser(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser]

    def delete(self, request, *args, **kwargs):
        try:
            user_id = request.data.get('id')

            if not user_id:
                return Response({
                    "success": False,
                    "message": "User ID is required."
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({
                    "success": False,
                    "message": "User not found."
                }, status=status.HTTP_404_NOT_FOUND)

            user.delete()
            return Response({
                "success": True,
                "message": "User deleted successfully."
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "An unexpected error occurred.",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserList(viewsets.ModelViewSet): # type: ignore
    pagination_class = None
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'id']


class DeleteAccountRequestViewSet(viewsets.ModelViewSet): # type: ignore
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = DeleteAccountRequest.objects.all()
    serializer_class = DeleteAccountRequestedSerializer

