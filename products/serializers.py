

from rest_framework import serializers
# from .models import ProductDetail
from api.models import *
from .models import *


class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.URLField(), write_only=True, required=False
    )
    class Meta:
        model = ProductDetail
        fields = "__all__"

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        product = ProductDetail.objects.create(**validated_data)
        for img_url in images:
            ProductImage.objects.create(product=product, image_url=img_url)
        return product

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['images'] = [img.image_url for img in instance.images.all()]
        return rep
    

class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = ProductDetail
        fields = "__all__"

    def get_images(self, obj):
        return [img.image_url for img in obj.images.all()]


    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']
