from django.conf import settings
from rest_framework import status
from django.shortcuts import  redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Appointment.models import Appointment
import stripe


stripe.api_key = settings.STRIP_SECRETE_KEY

class StripeCheckOutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, appointment_id):
        patient = request.user.patient

        print('-------------------------')
        print (appointment_id)
        print (patient)
        print('-------------------------')
        appointemts = Appointment.objects.get(id=appointment_id)
        print(appointemts.price)
        print('-------------------------')
        
        try:
            appointment = Appointment.objects.get(id=appointment_id)
            price = int(appointment.price * 100)  # Convert price to cents
            product_name = f"Appointment with {appointment.doctor}"
            
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': price,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.SITE_URL + '/reservations',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return Response({"url": checkout_session.url})
        except:
            return Response(
                {'error':'some thing went wrong while session checkout id'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )