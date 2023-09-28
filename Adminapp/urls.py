from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'movieslist', MovieViewSets)

urlpatterns = [
    # Other URL patterns
    path('', include(router.urls)),
    
]