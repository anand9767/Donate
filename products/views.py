from math import ceil
from rest_framework import generics
from rest_framework.filters import SearchFilter
from api.models import *
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from geopy.distance import distance
from rest_framework import pagination
from users.models import *
from .serializers import *
from api.models import *
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView

# Create your views here.


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


class MyProducts(ReadOnlyModelViewSet):
    queryset = ProductDetail.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    # Optional: use only if needed
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = {
        "id": ["in", "exact"],
        "user__id": ["in", "exact"],
        "title": ["in", "exact"],
        "category": ["in", "exact"],
        "sub_category": ["in", "exact"],
        "description": ["in", "exact"],
    }

    search_fields = ['title', 'category', 'sub_category', 'description']

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({
                    "success": True,
                    "message": "Products fetched successfully",
                    "data": serializer.data,
                })

            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "success": True,
                "message": "Products fetched successfully",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to fetch products",
                "error": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({
                "success": True,
                "message": "Product retrieved successfully",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

        except ProductDetail.DoesNotExist:
            return Response({
                "success": False,
                "message": "Product not found",
            }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to retrieve product",
                "error": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def calculateDistance(location1, location2):
    return ceil(distance(location1, location2).kilometers)


class Products(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')

        if not all([latitude, longitude, radius]):
            return ProductDetail.objects.none()

        try:
            latitude = float(latitude)
            longitude = float(longitude)
            radius = int(radius)

            all_products = ProductDetail.objects.exclude(
                latitude=None, longitude=None).order_by('-created_at')
            filtered_products = [
                product for product in all_products
                if calculateDistance((product.latitude, product.longitude), (latitude, longitude)) <= radius
            ]
            return filtered_products

        except ValueError:
            return ProductDetail.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if not queryset:
                return self.get_paginated_response({
                    "success": True,
                    "message": "No products found for the given location or invalid/missing parameters",
                    "data": [],
                })      
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response({
                    "success": True,
                    "message": "Products fetched successfully",
                    "data": serializer.data,
                })
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                "success": True,
                "message": "Products fetched successfully",
                "data": serializer.data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Something went wrong while fetching products",
                "error": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AddProductView(CreateAPIView):
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                "success": True,
                "message": "Product added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to add product",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateProduct(generics.UpdateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            images = request.data.get('images')

            serializer = self.get_serializer(
                instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            # Update images if provided
            if images is not None:
                instance.images.all().delete()
                for img_url in images:
                    ProductImage.objects.create(
                        product=instance, image_url=img_url)

            return Response({
                "success": True,
                "message": "Product updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to update product",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class DeleteProduct(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            product_id = request.data.get('id')
            if not product_id:
                return Response({
                    "success": False,
                    "message": "Missing 'id' in request body."
                }, status=status.HTTP_400_BAD_REQUEST)

            product = ProductDetail.objects.filter(id=product_id).first()
            if not product:
                return Response({
                    "success": False,
                    "message": f"No product found with id {product_id}"
                }, status=status.HTTP_404_NOT_FOUND)

            # Delete associated images
            product.images.all().delete()

            # Delete the product itself
            product.delete()

            return Response({
                "success": True,
                "message": "Product deleted successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Failed to delete product",
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
