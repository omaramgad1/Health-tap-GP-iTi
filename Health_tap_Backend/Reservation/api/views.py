from rest_framework.decorators  import  api_view, permission_classes
from rest_framework.response import Response
from Reservation.models import Reservation
from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated

@api_view()
@permission_classes([IsAuthenticated])
def reservation_list(request):
    reservations = Reservation.objects.all()
    serializer = ReservationSerializer(queryset=reservations)
    return Response(serializer)