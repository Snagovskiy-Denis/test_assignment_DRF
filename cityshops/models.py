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
