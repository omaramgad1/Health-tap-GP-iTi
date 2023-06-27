from django.db import models

from City.models import City


class District(models.Model):
    name_ar = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='districts')

    class Meta:
        verbose_name_plural = 'Districts'
        constraints = [
            models.UniqueConstraint(
                fields=['name_en', 'city'],
                name='unique_district_name_city_name_en'),
            models.UniqueConstraint(
                fields=['name_ar', 'city'],
                name='unique_district_name_city_name_ar')
        ]

    def __str__(self):
        return f'{self.name_en} ({self.city.name_en})'
