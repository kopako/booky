from django.db.models import Avg
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Feedback
from .serializers import ReadFeedbackSerializer, WriteFeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ReadFeedbackSerializer
        return WriteFeedbackSerializer

    def get_queryset(self):
        return Feedback.objects.select_related('rentee', 'advertisement')

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(rentee=self.request.user)

    @action(detail=True, methods=['get'], url_path='avg_rating')
    def avg_rating(self, request, pk=None):
        avg_rating = (Feedback.objects
        .filter(advertisement=pk)
        .aggregate(avg=Avg('rating_value'))['avg']
        )

        if avg_rating is None:
            return Response({"detail": "No ratings found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "advertisement_id": pk,
            "average_rating": round(avg_rating, 1)
        })

    @action(detail=True, methods=['get'], url_path='feedback')
    def for_ad(self, request, pk=None):
        feedbacks = (Feedback.objects.select_related('rentee', 'advertisement')
                     .filter(advertisement=pk)
                     )

        if not feedbacks:
            return Response({"detail": "No ratings found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReadFeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)
