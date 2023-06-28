from django.urls import path
from .views import appointment_list , appointment_detailes

urlpatterns = [
    # path('/', AppointmentView.as_view(), name='appointments'),
    path('/', appointment_list , name='appointment-list'),
    path('/<int:id>', appointment_detailes , name='appointment-detailes'),
]
