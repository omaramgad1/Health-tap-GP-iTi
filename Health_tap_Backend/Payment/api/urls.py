from django.urls import path

from .views import StripeCheckOutView
 
urlpatterns = [
    path('create-checkout-session/',StripeCheckOutView.as_view(),name='StripeCheckOutView'),
]
