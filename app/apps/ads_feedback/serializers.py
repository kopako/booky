from rest_framework import serializers


from .models import Feedback
from ..ads.models import Advertisement
from ..user.models.user import User


class WriteFeedbackSerializer(serializers.ModelSerializer):
    review_message = serializers.CharField(required=False)
    rating_value = serializers.IntegerField()
    advertisement = serializers.PrimaryKeyRelatedField(queryset=Advertisement.objects.all())

    class Meta:
        model = Feedback
        fields = ['advertisement', 'rating_value', 'review_message']


class ReadFeedbackSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(required=False)
    review_message = serializers.CharField(required=False)

    rentee = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Feedback
        fields = "__all__"