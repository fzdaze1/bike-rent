from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, BikeSerializer, RentalSerializer
from django.contrib.auth import get_user_model
from .models import Bike, Rental
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .tasks import calculate_rental_cost
from django.core.mail import send_mail
from django.conf import settings


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class BikeListView(generics.ListAPIView):
    serializer_class = BikeSerializer
    queryset = Bike.objects.filter(status='available')
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bike_rent(request, bike_id):
    user = request.user
    bike = Bike.objects.get(id=bike_id)
    if Rental.objects.filter(user=user, end_time__isnull=True).exists():
        return Response({'error': 'You can only rent one bike at a time.'}, status=400)
    if bike.status != 'available':
        return Response({'error': 'This bike is not available.'}, status=400)
    rental = Rental.objects.create(user=user, bike=bike)
    bike.status = 'rented'
    bike.save()
    return Response({'message': f'Bike {bike.id} rented successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bike_return(request, bike_id):
    user = request.user
    bike = Bike.objects.get(id=bike_id)
    if not Rental.objects.filter(user=user, end_time__isnull=True).exists():
        return Response({'error': 'You do not have an active rental.'}, status=400)
    try:
        rental = Rental.objects.get(
            user=user, bike=bike, end_time__isnull=True)
    except ObjectDoesNotExist:
        return Response({'error': 'You do not have an active rental for this bike.'}, status=400)
    calculate_rental_cost.delay(rental.id)
    bike.status = 'available'
    bike.save()
    subject = 'Bike Rental Return Confirmation'
    message = f'Hello {user.username},\n\nYour bike rental for bike {bike.name} has been successfully returned.'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    try:
        send_mail(subject, message, from_email, to_email)
    except Exception as e:
        return Response({'message': 'Bike returned successfully. Mail error'}, status=status.HTTP_200_OK)
    return Response({'message': 'Bike returned successfully.'}, status=status.HTTP_200_OK)


class RentalHistoryView(generics.ListAPIView):
    serializer_class = RentalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Rental.objects.filter(user=self.request.user)
