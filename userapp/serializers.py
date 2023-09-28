from rest_framework import serializers
from .models import User

from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email', 'password', 'name', 'phone', 'profile_image','is_active','is_owner')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        # Check if a new password is provided
        new_password = validated_data.get('password')
        if new_password:
            # Set and hash the new password
            instance.set_password(new_password)
        # Update other fields if provided
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)

        # Save the updated user instance
        instance.save()
        return instance


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'phone','email', 'profile_image','password')
        
        
class TheaterOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    def create (self,validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        validated_data["is_owner"]=True
        user=User(**validated_data)
        user.save()
        return user