from django.urls import path

from .views import StripeCheckOutView
 
urlpatterns = [
    path('create-checkout-session/<int:appointment_id>/',StripeCheckOutView.as_view(),name='StripeCheckOutView'),
]
