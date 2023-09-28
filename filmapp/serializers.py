from rest_framework import serializers
from .models import Movie
from Theaterapp.models import Theater,TimeSlot

class MovieSerializer(serializers.ModelSerializer):
    theaters = serializers.StringRelatedField(many=True)
    class Meta:
        model = Movie
        fields = '__all__'  # Include all fields from the Movie model

class MovieSerializerd(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'  # Include all fields from the Movie model
        


class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = '__all__'         
        
class TimeSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'     
        
class AddMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

class CreatTimeSlotSerializer(serializers.ModelSerializer):
    print('llllllllllllllllllll')
    class Meta:
        model = TimeSlot
        fields = '__all__'           