from django.shortcuts import render
from rest_framework.decorators import action
from filmapp.models import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import MovieSerializer,MovieSerializerd

# Create your views here.
class MovieViewSets(viewsets.ModelViewSet):
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