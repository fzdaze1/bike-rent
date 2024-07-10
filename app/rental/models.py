from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone


class CustomUser(AbstractUser):

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


User = get_user_model()


class Bike(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
    ]

    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='available')
    # ЗАВТРА СДЕЛАТЬ УНИКАЛЬНЫЕ ССЫЛКИ ДЛЯ БАЙКОВ slug = models.SlugField(max_length=255, db_index=True)


class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.bike} - {self.start_time} - {self.end_time}'
