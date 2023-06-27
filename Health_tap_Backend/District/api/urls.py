from django.urls import path
from .views import *

urlpatterns = [
    path('list-all/', get_districts, name='get_districts'),


]
