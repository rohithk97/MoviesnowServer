from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register(r'user',UserViewSet)
router.register(r'register-theater-owner', TheaterOwnerViewSet)
router.register(r'theater-owners-list',TheaterOwnerListView)

urlpatterns = [
    path('token/', AuthView.as_view(), name='token_obtain_pair'),
    # path('register/', UserRegistrationView.as_view(), name='user_registration'),
    # path('userlist/', UserListView.as_view(), name='user_list'),
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    # path('theater-owners-list/', TheaterOwnerListView.as_view({'get': 'list'}), name='theater-owner-list'),
    path('',include(router.urls)),

]