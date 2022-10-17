from django.shortcuts import render
from rest_framework import viewsets

from .utils import ResponseInfo
from .serializers import MenuItemSerializer,ItemSerializer
from .models import MenuItem,Item
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


#menuitems
class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(MenuItemViewSet,self).__init__(**kwargs)


    def list(self, request, *args, **kwargs):
        response_data = super(MenuItemViewSet, self).list(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        if not response_data.data:
            self.response_format['message'] = 'No Existing Menu Items'
        return Response(self.response_format)


    def create(self, request, *args, **kwargs):
        response_data = super(MenuItemViewSet, self).create(
                        request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = 201
        self.response_format['status'] = True
        self.response_format['message'] = 'New Menu Added'
        return Response(self.response_format)
                    

    def retrieve(self, request, *args, **kwargs):
        response_data = super(MenuItemViewSet, self).retrieve(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        if not response_data.data:
            self.response_format['message'] = 'Empty'
        else:
            self.response_format['message'] = 'Menu Items'
        return Response(self.response_format)

    def update(self, request, *args, **kwargs):
        response_data = super(MenuItemViewSet, self).update(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        self.response_format['message'] = 'Menu updated'
        return Response(self.response_format)

    def destroy(self, request, *args, **kwargs):
        response_data = super(MenuItemViewSet, self).destroy(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        self.response_format['message'] = 'Menu deleted'
        return Response(self.response_format)


#items
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['menuItem']

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(ItemViewSet,self).__init__(**kwargs)


    def list(self, request, *args, **kwargs):
        response_data = super(ItemViewSet, self).list(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        if not response_data.data:
            self.response_format['message'] = 'No Existing Items'
        return Response(self.response_format)


    def create(self, request, *args, **kwargs):
        response_data = super(ItemViewSet, self).create(
                        request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = 201
        self.response_format['status'] = True
        self.response_format['message'] = 'New Item Added'
        return Response(self.response_format)
                    

    def retrieve(self, request, *args, **kwargs):
        response_data = super(ItemViewSet, self).retrieve(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        if not response_data.data:
            self.response_format['message'] = 'Empty'
        else:
            self.response_format['message'] = 'Items'
        return Response(self.response_format)

    def update(self, request, *args, **kwargs):
        response_data = super(ItemViewSet, self).update(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        self.response_format['message'] = 'Item updated'
        return Response(self.response_format)

    def destroy(self, request, *args, **kwargs):
        response_data = super(ItemViewSet, self).destroy(
            request, *args, **kwargs)
        self.response_format['data'] = response_data.data
        self.response_format['statusCode'] = response_data.status_code
        self.response_format['status'] = True
        self.response_format['message'] = 'Item deleted'
        return Response(self.response_format)