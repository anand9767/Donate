from math import ceil, floor
from django.contrib.gis.measure import Distance,D
import io
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from multiprocessing import context
from select import select
from django.shortcuts import render
from api.models import ProductDetail
from rest_framework import generics, permissions
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.response import Response
from knox.models import AuthToken
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView
from rest_framework import viewsets
from .serializers import ProductSerialiser, UserSerializer, RegisterSerializer
from api import serializers
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import distance

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "message":"User Registered Successfully",
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })

#Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

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
           "message":"User Logged In Successfully",
           "user": userData.data
        })

class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['username']

    # user = User.objects.all()
    # print('user',request.user)
    # serializer = UserSerializer(user,many = True)
    # # print('serializers',User.objects.get(pk = user.pk))
    # json_data = JSONRenderer().render(serializer.data)
    # return HttpResponse(json_data,content_type = 'application/json')


class MyProducts(viewsets.ModelViewSet):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['userName','id']


class Products(viewsets.ModelViewSet):
     serializer_class = ProductSerialiser
     def get_queryset(self) :
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')
        # print('latitude123',latitude , longitude,radius)
        # dis = calculateDistance((13.0631,77.6207), (13.1155,77.1090))
        # print('distace ',ceil(dis))
        queryset = ProductDetail.objects.all()
        newqueryset = []
        for queryData in queryset.iterator():
            if(calculateDistance((queryData.latitude,queryData.longitude),(latitude,longitude)) <= int(radius)):
                newqueryset.append(queryData)
        return newqueryset

@csrf_exempt
def delete_Product(request):
    json_data = request.body
    stream = io.BytesIO(json_data)
    pythondata = JSONParser().parse(stream)
    id = pythondata.get('id')
    product = ProductDetail.objects.get(id=id)
    product.delete()
    return JsonResponse({'message':'Product Deleted'},safe=False)

@csrf_exempt
def delete_User(request):
    json_data = request.body
    stream = io.BytesIO(json_data)
    pythondata = JSONParser().parse(stream)
    id = pythondata.get('id')
    user = User.objects.get(id=id)
    user.delete()
    return JsonResponse({'message':'User Deleted'},safe=False)


def calculateDistance(location1,location2):
    return ceil(distance(location1, location2).kilometers)