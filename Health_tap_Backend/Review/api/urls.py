from django.urls import path
from .views import *

urlpatterns = [
    path('<int:doctor_id>/', list_all_reviews , name='list-all-reviews'),
    path('create/<int:doctor_id>/', create_review , name='create-reviews'),
]
