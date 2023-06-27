from django.urls import path
from .views import *

urlpatterns = [
    path('list-all/', get_cities, name='get_cities'),
    path('<int:city_id>/', get_city, name='get_city'),
    path('<int:city_id>/districts/',
         get_districts_by_city_id, name='get_districts_by_city_id'),
]
