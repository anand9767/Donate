from dataclasses import field, fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FCMTokens, MyChats, ProductDetail, RequestedProductDetail

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
    class Meta:
        model = ProductDetail
        fields = '__all__'


class MyChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyChats
        fields = '__all__'


class MyFCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMTokens
        fields = '__all__'


class RequestedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestedProductDetail
        fields = '__all__'


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
