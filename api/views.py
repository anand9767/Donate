from itertools import product
from math import ceil
from operator import ge
from rest_framework import status
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.contrib.gis.measure import Distance, D
import io
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.parsers import JSONParser
from multiprocessing import context
from select import select
from django.shortcuts import render
from api.models import FCMTokens, MyChats, ProductDetail, RequestedProductDetail
from rest_framework import generics, permissions
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.response import Response
from knox.models import AuthToken
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework import viewsets
from .serializers import ChangePasswordSerializer, MyChatsSerializer, MyFCMTokenSerializer, ProductSerializer, RequestedProductSerializer, UserSerializer, RegisterSerializer
from api import serializers
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import distance
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes, api_view


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "User Registered Successfully",
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Login API


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token = super(LoginAPI, self).post(request, format=None)
        id = User.objects.get(pk=user.pk)
        userData = UserSerializer(id)
        json_data = JSONRenderer().render(userData.data)
        # return HttpResponse(json_data,content_type = 'application/json')
        return Response({
            "message": "User Logged In Successfully",
            "user": userData.data
        })


class UserList(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'id']


class MyProducts(viewsets.ModelViewSet):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    queryset = ProductDetail.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['userName', 'id']
    search_fields = ['title', 'category', 'sub_category']


class MyRequestedProducts(viewsets.ModelViewSet):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    queryset = RequestedProductDetail.objects.all()
    serializer_class = RequestedProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['userName', 'id']
    search_fields = ['title', 'category', 'sub_category']


class Chats(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    queryset = MyChats.objects.all()
    serializer_class = MyChatsSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['intiatorId', 'friendId']


class Products(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    serializer_class = ProductSerializer

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')
        queryset = ProductDetail.objects.all()
        print('query set', queryset)
        newqueryset = []
        for queryData in queryset.iterator():
            if (calculateDistance((queryData.latitude, queryData.longitude), (latitude, longitude)) <= int(radius)):
                newqueryset.append(queryData)
        return newqueryset


class RequestedProducts(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    serializer_class = RequestedProductSerializer

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')
        queryset = RequestedProductDetail.objects.all()
        print('query set', queryset)
        newqueryset = []
        for queryData in queryset.iterator():
            if (calculateDistance((queryData.latitude, queryData.longitude), (latitude, longitude)) <= int(radius)):
                newqueryset.append(queryData)
        return newqueryset


@csrf_exempt
@api_view(['DELETE'])
# @authentication_classes((authentication.TokenAuthentication,))
# @permission_classes((permissions.IsAuthenticated,))
def delete_product(request, format=None):
    json_data = request.body
    stream = io.BytesIO(json_data)
    pythondata = JSONParser().parse(stream)
    id = pythondata.get('id')
    product = ProductDetail.objects.get(id=id)
    product.delete()
    return JsonResponse({'message': 'Product Deleted'}, safe=False)


@csrf_exempt
@api_view(['DELETE'])
# @authentication_classes((authentication.TokenAuthentication,))
# @permission_classes((permissions.IsAuthenticated,))
def delete_requested_product(request, format=None):
    json_data = request.body
    stream = io.BytesIO(json_data)
    pythondata = JSONParser().parse(stream)
    id = pythondata.get('id')
    product = RequestedProductDetail.objects.get(id=id)
    product.delete()
    return JsonResponse({'message': 'Product Deleted'}, safe=False)


@csrf_exempt
@api_view(['DELETE'])
# @authentication_classes((authentication.TokenAuthentication,))
# @permission_classes((permissions.IsAuthenticated,))
def delete_user(request, format=None):
    json_data = request.body
    stream = io.BytesIO(json_data)
    pythondata = JSONParser().parse(stream)
    id = pythondata.get('id')
    user = User.objects.get(id=id)
    user.delete()
    return JsonResponse({'message': 'User Deleted'}, safe=False)


class UpdateProduct(generics.UpdateAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        product = ProductDetail.objects.get(id=id)
        serializer = ProductSerializer(product, data=pythondata, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'message': 'Data Updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


class UpdateUser(generics.UpdateAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=pythondata, partial=True)
        if serializer.is_valid():
            serializer.save()
            res = {'message': 'User Updated'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type='application/json')


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            # if not self.object.check_password(serializer.data.get("old_password")):
            #     return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrUpdateFCMToken(generics.ListCreateAPIView):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    queryset = FCMTokens.objects.all()
    serializer_class = MyFCMTokenSerializer

    def create(self, request, *args, **kwargs):
        myModel, created = FCMTokens.objects.update_or_create(userId=request.data['userId'],
                                                              defaults={
            'token': request.data['token'],
            'timestamp': request.data['timestamp']
        })
        serializer = MyFCMTokenSerializer(
            myModel, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()

        if created:
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status.HTTP_200_OK)


class GetFCMToken(viewsets.ModelViewSet):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_class = [permissions.IsAuthenticated]

    queryset = FCMTokens.objects.all()
    serializer_class = MyFCMTokenSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userId']


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


def calculateDistance(location1, location2):
    return ceil(distance(location1, location2).kilometers)
