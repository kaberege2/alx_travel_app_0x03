from rest_framework import routers 
from django.urls import path, include
from .views import BookingViewSet, ListingViewSet

router = routers.DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'listings', ListingViewSet, basename='listing')

urlpatterns = [
    path('', include(router.urls)),
]
