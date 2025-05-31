# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import DonationStory
from .serializers import DonationStorySerializer


class DonationStoryViewSet(viewsets.ModelViewSet):
    serializer_class = DonationStorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_queryset(self):
        # Show only approved stories publicly
        return DonationStory.objects.filter(is_approved=True).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"message": "You do not have permission to delete this story."},
                            status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response({"message": "Story deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class DonationStoryAdminViewSet(viewsets.ModelViewSet):
    queryset = DonationStory.objects.all().order_by('-created_at')
    serializer_class = DonationStorySerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        try:
            story = self.get_object()
            story.is_approved = True
            story.save()
            return Response({"message": "Story approved."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "An error occurred", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
