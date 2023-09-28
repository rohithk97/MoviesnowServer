from rest_framework.serializers import ModelSerializer,Serializer, StringRelatedField
from .models import Theater,Seat,Booking,Payment
from rest_framework import serializers

class TheaterSerializer(ModelSerializer):
    owner = StringRelatedField()
    
    class Meta:
        model = Theater
        fields = '__all__'
        
        
        
class TheaterRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = '__all__'
    def create (self,validated_data):
        
        validated_data["approved"]=True
        theater = Theater(**validated_data)
        theater.save()

        return theater     
    
    
    
        
class SeatSerializer(ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class BookingSerializer(ModelSerializer):
    user = StringRelatedField()
    theater = StringRelatedField()
    movie = StringRelatedField()
    print(movie,'ppppppppppppppppppppppppp')
    class Meta:
        model = Booking
        fields = '__all__'        
        
class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'        