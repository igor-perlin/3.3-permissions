from rest_framework import serializers
from .models import Advertisement
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Advertisement

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at']

    def validate(self, data):
        # Ограничение на количество открытых объявлений
        if self.context['request'].method == 'POST':
            user = self.context['request'].user
            open_ads_count = Advertisement.objects.filter(creator=user, status='OPEN').count()
            if open_ads_count >= 10:
                raise ValidationError({"detail": "Нельзя иметь более 10 открытых объявлений."})
        return data

    def update(self, instance, validated_data):
        # Проверка, что только автор может обновить объявление
        if instance.creator != self.context['request'].user:
            raise PermissionDenied({"detail": "Только автор может обновить это объявление."})
        return super().update(instance, validated_data)


