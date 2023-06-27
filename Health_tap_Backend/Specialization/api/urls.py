from django.urls import path
<<<<<<< HEAD
from .views import *

urlpatterns = [

]
=======
from Specialization.api.views import SpecializationListCreateView

urlpatterns = [
    path('', SpecializationListCreateView.as_view(), name='specialization-list-create'),
]
>>>>>>> aa1979b0426c63620f331414a9dd63dd206c0d3a
