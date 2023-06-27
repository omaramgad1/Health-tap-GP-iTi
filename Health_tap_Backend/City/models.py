from django.db import models


class City(models.Model):
    name_ar = models.CharField(max_length=255, unique=True)
    name_en = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name_en
