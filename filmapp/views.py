from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Movie
from .serializers import MovieSerializer,MovieSerializerd
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from Theaterapp.models import Theater, TimeSlot
from rest_framework.decorators import api_view
from rest_framework.decorators import action

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieSerializerd
    # permission_classes = [IsAdminUser]  # Only allow admin users to perform CRUD operations on movies
    
    # @action(detail=True, methods=['post'])
    # def block(self, request, pk=None):
    #     movie = self.get_object()
    #     movie.is_active = False
    #     movie.save()
    #     return Response(status=status.HTTP_200_OK)

    # @action(detail=True, methods=['post'])
    # def unblock(self, request, pk=None):
    #     movie = self.get_object()
    #     movie.is_active = True
    #     movie.save()
    #     return Response(status=status.HTTP_200_OK)
    
class MovieViewSetAdmin(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerd
    # permission_classes = [IsAdminUser]  # Only allow admin users to perform CRUD operations on movies
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        movie = self.get_object()
        movie.is_active = False
        movie.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        movie = self.get_object()
        movie.is_active = True
        movie.save()
        return Response(status=status.HTTP_200_OK)


# class MovieDetail(APIView):
#     def get(self, request, movie_id):
#         movie = Movie.objects.filter(id=movie_id).first()
#         if movie is not None:
#             serializer = MovieSerializer(movie)
#             return Response(serializer.data)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)

class MovietheaterViewSet(APIView):
    def get(self, request, movie_id):
        theaters = Theater.objects.filter(movies__id=movie_id)
        movie = Movie.objects.filter(id=movie_id).first()

        if movie is not None:
            movieserializer = MovieSerializer(movie)
        else:
            return Response({"message": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)

        theater_data = []

        for theater in theaters:
            theater_serializer = TheaterSerializer(theater)

            # Retrieve time slots for the current movie and theater
            time_slots = TimeSlot.objects.filter(movie=movie, theater=theater)
            time_slot_data = TimeSlotSerializer(time_slots, many=True).data

            # Add the time slot data to the theater serializer
            theater_data.append({
                **theater_serializer.data,
                'time_slots': time_slot_data
            })

        data = {
            'film': movieserializer.data,
            'movietheaters': theater_data
        }

        return Response(data)



# class AddMovieView(APIView):
    
#     def post(self, request):
#         serializer = AddMovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddMovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = AddMovieSerializer
    

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        print(serializer,'ddddddddddddddddddddddddddd')
        if serializer.is_valid():
            serializer.save()
            print(serializer,"eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class AssignMovieToTheaterView(APIView):
    def post(self, request, theater_id):
        try:
            movie_title = request.data.get('movieTitle')
            print("Received movie title:", movie_title)

            # Check if the movie exists or create a new one
            movie, created = Movie.objects.get_or_create(title=movie_title)

            # Fetch the theater based on theater_id
            theater = Theater.objects.get(id=theater_id)
            print("Theater:", theater)

            # Assign the movie to the theater
            theater.movies.add(movie)

            return Response({'message': 'Movie assigned to theater successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print("Error:", str(e))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        

class CreateTimeSlotsView(APIView):
    def post(self, request):
        try:
            data = request.data
            time_slots_str = data['timeSlots'][0]  # Assuming there's only one string in the list
            time_slots_list = [time.strip() for time in time_slots_str.split(',')]
            print(data, "dataaaaaaaaaaaaaaaaaaaaaaaa")
            movie = Movie.objects.filter(title=data['movieTitle']).first()
            for time in time_slots_list:
                slots = {
                    'movie':movie.id,
                    'slot_time': time,
                    'theater': data['theater']
                }
                serializer = CreatTimeSlotSerializer(data=slots)
                print(slots,'seriaaaaaaaaaaaaaaaaa')
                if serializer.is_valid():
                    print('validddddddddddddddddddddd')
                    serializer.save()
                else:
                    print('eroooooooooooooooooooooooooo')
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)  

        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error creating time slots: {str(e)}")
            return Response({"error": "An error occurred while creating time slots."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   