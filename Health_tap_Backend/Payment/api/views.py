from django.conf import settings
from rest_framework import status
from django.shortcuts import  redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Appointment.models import Appointment
from Reservation.models import Reservation
from Reservation.api.serializers import ReservationSerializer
import stripe


stripe.api_key = settings.STRIP_SECRETE_KEY

class StripeCheckOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, appointment_id):
        patient = request.user.patient

        try:
            appointment = Appointment.objects.get(id=appointment_id)

            # Check if the appointment is available
            if appointment.status != 'A':
                return Response({'error': 'Appointment is not available.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Calculate the price in cents
            price = int(appointment.price * 100)

            # Create the reservation
            reservation = Reservation.objects.create(patient=patient, appointment=appointment, status='R')

            # Update the appointment status to 'R'
            appointment.status = 'R'
            appointment.save()

            # Create the Stripe checkout session
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

            # Serialize the reservation and return the checkout session URL
            serializer = ReservationSerializer(reservation)
            return Response({"url": checkout_session.url, "reservation": serializer.data})
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)