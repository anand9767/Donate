from itertools import product
from math import ceil
from operator import ge
from rest_framework import status
from rest_framework import generics
from rest_framework.filters import SearchFilter
from django.contrib.gis.measure import Distance,D
import io
from django.views.decorators.csrf import csrf_exempt,csrf_protect
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
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView,GenericAPIView
from rest_framework.mixins import DestroyModelMixin
from rest_framework import viewsets
from .serializers import ChangePasswordSerializer, ProductSerialiser, UserSerializer, RegisterSerializer
from api import serializers
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import distance
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response   
from rest_framework.decorators import permission_classes,authentication_classes,api_view


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]

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

    authentication_classes = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]

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
    authentication_classes = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username','id']


class MyProducts(viewsets.ModelViewSet):
    
    authentication_classes = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]

    queryset = ProductDetail.objects.all()
    serializer_class = ProductSerialiser

    filter_backends = [DjangoFilterBackend,SearchFilter]
    filterset_fields = ['userName','id']
    search_fields = ['title','category','sub_category']


    # def list(self, request):
    #     queryset = ProductDetail.objects.all()
    #     serializer = ProductSerialiser(queryset, many=True)
    #     return Response({
    #         'message':'success',
    #         'data':serializer.data})

    # def retrieve(self, request, pk=None):  
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response({'data':serializer.data})


class Products(viewsets.ModelViewSet):
     authentication_classes = [authentication.TokenAuthentication]
     permission_class = [permissions.IsAuthenticated]

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
@api_view(['DELETE'])
@authentication_classes((authentication.TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def delete_product(request,format=None):
    json_data = request.body
    stream = io.BytesIO(json_data)
    pythondata = JSONParser().parse(stream)
    id = pythondata.get('id')
    product = ProductDetail.objects.get(id=id)
    product.delete()
    return JsonResponse({'message':'Product Deleted'},safe=False)

@csrf_exempt
@api_view(['DELETE'])
@authentication_classes((authentication.TokenAuthentication,))
@permission_classes((permissions.IsAuthenticated,))
def delete_user(request,format = None):
    json_data = request.body
    stream = io.BytesIO(json_data)
    pythondata = JSONParser().parse(stream)
    id = pythondata.get('id')
    user = User.objects.get(id=id)
    user.delete()
    return JsonResponse({'message':'User Deleted'},safe=False)

    
class UpdateProduct(generics.UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        product = ProductDetail.objects.get(id= id)
        serializer = ProductSerialiser(product,data = pythondata,partial= True)
        if serializer.is_valid():
                serializer.save()
                res = {'message': 'Data Updated'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data,content_type = 'application/json')

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type = 'application/json')

class UpdateUser(generics.UpdateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_class = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        user = User.objects.get(id= id)
        serializer = UserSerializer(user,data = pythondata,partial= True)
        if serializer.is_valid():
                serializer.save()
                res = {'message': 'User Updated'}
                json_data = JSONRenderer().render(res)
                return HttpResponse(json_data,content_type = 'application/json')

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data,content_type = 'application/json')


class ChangePasswordView(generics.UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = User

        authentication_classes = [authentication.TokenAuthentication]
        permission_class = [permissions.IsAuthenticated]

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


def calculateDistance(location1,location2):
    return ceil(distance(location1, location2).kilometers)