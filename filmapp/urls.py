from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from . import views

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'moviesadmin',MovieViewSetAdmin)
router.register(r'addmovies',AddMovieView)

urlpatterns = [
    # Other URL patterns
    path('', include(router.urls)),
    path('moviedetail/<int:movie_id>/',MovietheaterViewSet.as_view(),),
    # path('movies/add/',AddMovieView.as_view(), name='add_movie'),
    path('assign_movie/<int:theater_id>/', AssignMovieToTheaterView.as_view(), name='assign_movie_to_theater'),
    path('create_time_slots/', CreateTimeSlotsView.as_view(), name='create_time_slots'),
]
