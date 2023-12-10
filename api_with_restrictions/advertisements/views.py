from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement
from .serializers import AdvertisementSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied
from .filters import AdvertisementFilter
from django_filters.rest_framework import DjangoFilterBackend

class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    filter_backends = [DjangoFilterBackend]

    def perform_create(self, serializer):
        if Advertisement.objects.filter(creator=self.request.user, status='OPEN').count() >= 10:
            raise ValidationError({'detail': 'Нельзя открывать больше 10 объявлений'})
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        advertisement = self.get_object()
        if advertisement.creator != self.request.user:
            raise PermissionDenied({'detail': 'Можно обновлять только свои объявления'})
        serializer.save()

    def perform_destroy(self, instance):
        if instance.creator != self.request.user:
            raise PermissionDenied({'detail': 'Удалять можно только свои объявления'})
        instance.delete()

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update"]:
            return [IsAuthenticated()]
        return []
