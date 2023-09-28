from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import update_session_auth_hash
from rest_framework.decorators import action
# from .serializers import UserSerializer 

# Create your views here.
class AuthView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)   
        token = response.data['access']
        refresh=response.data['access']
        response.data['accessToken'] = token
        response.data['refreshToken'] = refresh
        response.data.pop('access', None)
        response.data.pop('refresh', None)
        email = request.data.get('email')
        user = User.objects.get(email=email)
        response.data['user'] = {
            "name" : str(user.name),
            "email" : str(user.email),
            "Admin" : str(user.is_admin)
        }
        
        print()
        return response
    
    
# class UserRegistrationView(APIView):
#     def post(self, request, format=None):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.filter(is_admin=False,is_owner=False)
    serializer_class=UserSerializer
    
    
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)
    
      

class TheaterOwnerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = TheaterOwnerSerializer
    # def create(self, request):
    #     serializer = TheaterOwnerRegistrationSerializer()
    #     print(request.data)
    #     if serializer.is_valid():
    #         # Set is_owner to True
    #         serializer.validated_data['is_owner'] = True

    #         # Create the theater owner user
    #         # Ensure you set the password correctly
    #         user = User.objects.create_user(
    #             email=serializer.validated_data['email'],
    #             password=serializer.validated_data['password'],
    #             phone=serializer.validated_data['phone'],
    #             business_name=serializer.validated_data['business_name'],
    #             business_address=serializer.validated_data['business_address'],
    #             business_license_number=serializer.validated_data['business_license_number'],
    #             is_owner=True,  # Set is_owner to True
    #         )

    #         return Response({'message': 'Theater owner registered successfully'}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TheaterOwnerListView(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_owner=True)
    serializer_class = TheaterOwnerSerializer   
     
    @action(detail=True, methods=['post'])
    def block(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def unblock(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        
        user.save()
        return Response(status=status.HTTP_200_OK)
    
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import User
# from .serializers import UserSerializer  # Import your UserSerializer

# class UserListView(APIView):
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)  # Use your UserSerializer
#         return Response(serializer.data, status=status.HTTP_200_OK)

    
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Adjust the permission classes as needed

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)  
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)

        if serializer.is_valid():
            # Check if a new password is provided
            new_password = request.data.get("new_password")
            if new_password:
                # Check the current password
                current_password = request.data.get("current_password")
                if not request.user.check_password(current_password):
                    return Response(
                        {"current_password": ["Incorrect current password"]},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Set and hash the new password
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Keep the user logged in
                return Response({"message": "Password updated successfully"})

            # For other profile updates, save the serializer data
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)