from django.urls import path
from .views import *

urlpatterns = [
    path('', list_all_reservation , name='list_all_reservation'),
    path('patient/list/reserved/', list_reserved_reservation , name='list-reserved-reservation'),
    # path('doctor/list/cancelled/', list_cancelled_reservation, name='list-cancelled-reservation'),
    path('patient/list/Done/', list_done_reservation, name='list-done-reservation'),
    path('patient/list/<int:reservation_id>/', list_specific_reservation, name='list-specific-reservation'),
    path('patient/create/<int:appointment_pk>/', create_reservation, name='create-reservation'),
    path('patient/delete/<int:reservation_pk>/', delete_reservation, name='delete-reservation'),
    path('patient/list/<int:reservation_pk>/cancel', cancel_reservation , name='delete-reservation'),
    
    # path('/<int:id>', appointment_detailes , name='appointment-detailes'),
]
