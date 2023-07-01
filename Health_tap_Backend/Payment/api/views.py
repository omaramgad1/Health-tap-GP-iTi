from django.conf import settings
from rest_framework import status
from django.shortcuts import  redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Reservation.models import Reservation
import stripe


stripe.api_key = settings.STRIP_SECRETE_KEY

class StripeCheckOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # user_info = request.data 
        # user_id = user_info.get('user_id')
        
        # print(user_id)
        # print('-------------------------')
        # reservations = Cart.objects.get(user_id)
        # cart_items = CartItems.objects.filter(cart=cart)
        patient = request.user.patient
        print ('********************************')
        print(patient)
        print ('********************************')
        reservations = Reservation.objects.filter(patient=patient)
        print ('********************************')
        print(reservations)
        print ('********************************')
        
        line_items = []
        for item in reservations:
            product_name = item.id
            
            price = item.product.price * 100  # Stripe requires the price in cents
            line_item = {
                'price_data' :{
                    'currency' : 'usd',  
                    'reservation_data': {
                        'name': product_name,
                    },
                    'unit_amount': int(price)
                },
                'quantity' : item.quantity
            }
            line_items.append(line_item)
        try:                
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                # success_url=settings.SITE_URL + '/?success=true/' + 'session_id={CHECKOUT_SESSION_ID}',
                success_url=settings.SITE_URL + '/reservation',
                cancel_url=settings.SITE_URL  + '?canceled=true',
                
            )
            return redirect(checkout_session.url)
        except:
            return Response(
                {'error':'some thing went wrong while session checkout id'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )