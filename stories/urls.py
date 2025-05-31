# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationStoryViewSet, DonationStoryAdminViewSet

router = DefaultRouter()
router.register(r'stories', DonationStoryViewSet, basename='stories')
router.register(r'admin/stories', DonationStoryAdminViewSet,
                basename='admin-stories')

urlpatterns = [
    path('', include(router.urls)),
]
