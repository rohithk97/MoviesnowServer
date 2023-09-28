from rest_framework import serializers
from filmapp.models import Movie

class MovieSerializerd(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__' 