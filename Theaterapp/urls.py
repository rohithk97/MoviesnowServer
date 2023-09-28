from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router=DefaultRouter()
router.register(r'theaters',TheaterViewSet)
# router.register(r'theaterupdate', TheaterUpdateViewSet)
# router.register(r'register-theater', TheaterRegisterViewSet)

urlpatterns = [
    path('list/', TheaterViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', TheaterViewSet.as_view({'get': 'retrieve', 'put': 'update','patch': 'partial_update', 'delete':'destroy'})),   
    path('ownertheaters/', OwnerTheaters.as_view(), name='owner_theaters'),
    path('theaterdetail/', TheaterDetailView.as_view(), name='theater_detail'),
    path('register-theater/', TheaterRegistration.as_view(), name='register_theater'),
    path('seats/', SeatListView.as_view(), name='seat-list'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('reservation/', ReservationView.as_view(), name='reservation'),
    path('occupiedseats/', OccupiedSeatsView.as_view(), name='occupied-seats'),
    path('admin/bookings/', AdminBookingListView.as_view(), name='admin-booking-list'),
    # path('theater/block/<int:pk>/', TheaterViewSet.as_view({'post': 'block'})),
    # path('theater/unblock/<int:pk>/', TheaterViewSet.as_view({'post': 'unblock'})),
    # path('theaterupdate/<int:id>/', TheaterUpdateView.as_view(), name='theater-update'),
    path('theaterupdate/<int:pk>/', TheaterUpdateAPIView.as_view(), name='theater-update'),
    path('cancel-booking/<int:booking_id>/', CancelBookingView.as_view(), name='cancel-booking'),
    path('',include(router.urls)),
]   