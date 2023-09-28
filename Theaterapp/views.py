from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateAPIView
from userapp.models import User
# Create your views here.
from rest_framework.permissions import BasePermission,SAFE_METHODS,IsAdminUser
from rest_framework import viewsets,status
from rest_framework.views import APIView
from rest_framework.decorators import action
from .models import Theater
from .models import Seat
from filmapp.models import Movie
from .models import Booking,Payment
from .serializers import TheaterSerializer,SeatSerializer,BookingSerializer,PaymentSerializer,TheaterRegisterSerializer
from rest_framework.response import Response
from django.views.generic import DetailView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.http import Http404 
# from .permissions import IsOwnerOrAdmin


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.method in SAFE_METHODS)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or (request.method in SAFE_METHODS or obj.owner == request.user)
    
    
    
class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.filter()
    serializer_class = TheaterSerializer
    # permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        theater = self.get_object()
        theater.is_active = False  # Update the field to block the theater
        theater.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        theater = self.get_object()
        theater.is_active = True # Update the field to unblock the theater
        theater.save()
        return Response(status=status.HTTP_200_OK)
    
    
    
    
class OwnerTheaters(APIView):
    def get(self, request):
        email = request.query_params.get('email', None)
        if email:
            theaters = Theater.objects.filter(owner__email=email)
            serializer = TheaterSerializer(theaters, many=True)
            return Response(serializer.data)
        return Response({"message": "Please provide a valid email parameter."}, status=400)
    
    
    
class TheaterUpdateAPIView(APIView):
    def get_object(self, pk):
        try:
            return Theater.objects.get(pk=pk)
        except Theater.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        theater = self.get_object(pk)
        serializer = TheaterSerializer(theater)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        theater = self.get_object(pk)
        serializer = TheaterSerializer(theater, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class TheaterDetailView(APIView):

    def get(self, request): 
        id = request.query_params.get('id', None)
        try:
            theater = Theater.objects.get(pk=id)
            serializer = TheaterSerializer(theater)  # Assuming you have a serializer for the Theater model
            return Response(serializer.data)
        except Theater.DoesNotExist:
            return Response({'error': 'Theater not found'}, status=status.HTTP_404_NOT_FOUND)
   
   
class TheaterRegistration(APIView):
    # authentication_classes = [SessionAuthentication]  # Use appropriate authentication classes as per your project's settings
    # permission_classes = [IsAuthenticated]  # Ensure the user making the request is authenticated

    def post(self, request):
        print(request.data['email'],'[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]')
        email = request.data['email'] 
        user = User.objects.get(email=email)
        serializer = TheaterSerializer(data=request.data)
        if serializer.is_valid():
            # Assign the logged-in user as the owner of the theater
            serializer.save(owner= user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors,'[[[ooooooooooooooooooooooooo444444444oooooooooooooooooooooooo]]]')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
       
class TheaterRegisterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class =TheaterRegisterSerializer    
    
    
    
    
    
    
    
class SeatListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seats = Seat.objects.all()
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SeatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter bookings based on the current user's ID
        user_bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(user_bookings, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Set the user field in the serializer to the current user
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == 'Cancelled':
            return Response({'error': 'Booking is already cancelled'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the booking status using the serializer
        serializer = BookingSerializer(booking, data={'status': 'Cancelled'}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking successfully cancelled'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    
    
class AdminBookingListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Retrieve all bookings for admin
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)    
    
    
    
import json
    
class ReservationView(APIView):    
    permission_classes = [AllowAny]
    def post(self, request):
        if request.data is not None:
            print(request.data,'leklklkelokolkolkolo')
            email = json.loads(request.data['user'])
            print(email['email'],'eeeeeeeeeeeeeee')
            user = User.objects.get(email=email['email'])
            theater = Theater.objects.get(name=request.data['theater'])
            print(int(request.data['movie']),'ttttttttttttttttttttttttttttt')
            # data = {
            #     'user': int(user.id),
            #     'movie' : int(request.data['movie']),
                
            #     'theater' :theater.id,
            #     'seats_booked':request.data['seats_booked'],
            #     'time':request.data['time'],
            #     'date': request.data['date']
            # }
            movie =Movie.objects.get(id=int(request.data['movie']))
            theater =Theater.objects.get(id=theater.id)
            data = Booking.objects.create(
                user=user,
                movie=movie,
                theater=theater,
                seats_booked=request.data['seats_booked'],
                date=request.data['date'],
                time=request.data['time'],
                )
            print(data,'dataaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            serializer = BookingSerializer(data=data)
       
            print(request.data['payment_id'],'qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
            payment_data={
                'amount':request.data['total_price'],
                'payment_id':request.data['payment_id'],
                'bookings':  data.id 
            }
            print( payment_data,'dataaaaaaa payment_dataaaaaaaaaaaaaaaaa')
            paymentSerializer=PaymentSerializer(data=payment_data)
            if paymentSerializer.is_valid():
                print('uuuuuuuuuuuuuuuuuuuuuuuuuu')
                paymentSerializer.save()
            else:
                print(paymentSerializer.errors,'kollpoooooooooooooooooooookkkkkkkk')
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors,'ghjhghjhgjijikkkkkkkkkkkkkkk')
        return Response( status=status.HTTP_400_BAD_REQUEST)   
    
    
class OccupiedSeatsView(APIView):
    def get(self, request):
        try:
            theater_id = request.GET.get('theater_id')
            movie_id = request.GET.get('movie_id')
            time = request.GET.get('time')
            date = request.GET.get('date')
            
            # Perform validation on the received parameters if needed

            # Query the database to get occupied seats based on provided parameters
            occupied_seats = Booking.objects.filter(
            theater_id=theater_id,
            movie_id=movie_id,
            time=time,
            date=date,
            ).values_list('seats_booked', flat=True)

            # Use list comprehension to flatten the list
            occupied_seats = [seat for seats in occupied_seats for seat in seats]

            # Return the flattened list of occupied seats as JSON response
            return Response(occupied_seats, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    