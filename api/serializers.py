from dataclasses import field, fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MyChats, ProductDetail

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name' ,'email','date_joined')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username','first_name','last_name','email', 'password','date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],first_name=validated_data['first_name'],last_name= validated_data['last_name'],email= validated_data['email'],password= validated_data['password'],date_joined=validated_data['date_joined'])

        return user

class ProductSerialiser(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ['id','title','description','image','latitude','longitude','number','email','contact_comments','category','sub_category','extra_comments','timeStamp','userId','userName','name']

class MyChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyChats
        fields = ['id','intiatorId','friendId','friendName','lastMessage','timeStampMessage','timeStampChat']

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required = True)
    new_password = serializers.CharField(required=True)