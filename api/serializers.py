from dataclasses import field, fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

# User Serializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email', 'date_joined')

# Register Serializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name',
                  'email', 'password', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        email=validated_data['email'], password=validated_data['password'], date_joined=validated_data['date_joined'])

        return user


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductDetail
        fields = ('id', 'title', 'description', 'image', 'latitude', 'longitude', 'number', 'email',
                  'contact_comments', 'category', 'sub_category', 'extra_comments', 'timeStamp', 'user', 'name', 'user_id')
        extra_kwargs = {
            'user_id': {'source': 'user', 'write_only': True},
        }


class MyChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyChats
        fields = '__all__'


class MyFCMTokenSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = FCMTokens
        fields = ('token','timestamp', 'user','user_id')
        extra_kwargs = {
            'user_id': {'source': 'user', 'write_only': True},
        }


class RequestedProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = RequestedProductDetail
        fields = ('id', 'title', 'description', 'latitude', 'longitude', 'number', 'email',
                   'category', 'sub_category', 'timeStamp', 'user', 'name', 'user_id')
        extra_kwargs = {
            'user_id': {'source': 'user', 'write_only': True},
        }

class DeleteAccountRequestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteAccountRequest
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
