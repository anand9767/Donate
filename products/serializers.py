

from rest_framework import serializers
# from .models import ProductDetail
from api.models import *


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        exclude = ['created_at', 'updated_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        return ProductDetail.objects.create(**validated_data)
