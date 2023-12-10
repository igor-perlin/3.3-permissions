from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""
    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"


class Advertisement(models.Model):
    """Объявление."""
    STATUS_CHOICES = [('OPEN', 'Open'), ('CLOSED', 'Closed')]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=6,
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='advertisements'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
