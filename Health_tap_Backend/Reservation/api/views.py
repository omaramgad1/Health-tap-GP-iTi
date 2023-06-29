from rest_framework.decorators  import  api_view, permission_classes
from rest_framework.response import Response
from Reservation.models import Reservation
from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_reservation(request):
    reservations = Reservation.objects.all()
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_reserved_reservation(request):
    reservations = Reservation.objects.filter(status='R')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_cancelled_reservation(request):
    reservations = Reservation.objects.filter(status='C')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_done_reservation(request):
    reservations = Reservation.objects.filter(status='D')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

