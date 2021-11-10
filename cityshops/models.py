from django.core.exceptions import ValidationError
from django.utils import timezone

from django.db import models


class City(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self) -> str:
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'city')  # no duplicate streets in a city

    def __str__(self) -> str:
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=256)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    house_numbers = models.CharField(max_length=16)  # alphanumeric + specials
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self) -> str:
        return self.name

    def clean(self):
        if self.closing_time < self.opening_time:
            raise ValidationError('Shop cannot have closing time earlier than opening time')

    def is_closed(self) -> bool:
        return not self.is_opened()

    def is_opened(self) -> bool:
        now = timezone.now().time()
        return self.opening_time <= now < self.closing_time
