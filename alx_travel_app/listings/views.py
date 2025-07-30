from rest_framework import status, viewsets
from rest_framework.response import Response
from .permissions import IsAuthenticatedIsOwnerOrReadOnlyListing, IsAuthenticatedIsOwnerBooking
from django.contrib.auth import get_user_model
from .serializers import BookingSerializer, ListingSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Booking, Listing

User = get_user_model()  # Custom user model

# Booking view
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedIsOwnerBooking]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="List user's bookings",
        operation_description="Retrieve a list of all bookings made by the authenticated user."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a booking",
        operation_description="Create a new booking for a property. The booking will be associated with the authenticated user."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a booking",
        operation_description="Retrieve details of a specific booking made by the authenticated user."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a booking",
        operation_description="Update all details of an existing booking. Only the booking owner can perform this action."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a booking",
        operation_description="Update one or more fields of an existing booking. Only the booking owner can perform this action."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Cancel a booking",
        operation_description="Delete (cancel) an existing booking. Only the booking owner can perform this action."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

# Listing view
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedIsOwnerOrReadOnlyListing]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)

    @swagger_auto_schema(
        operation_summary="List all properties",
        operation_description="Retrieve a list of all available property listings."
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a property listing",
        operation_description="Create a new property listing. The listing will be associated with the authenticated user as the host."
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve a property",
        operation_description="Retrieve details of a specific property listing."
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a property listing",
        operation_description="Update all details of an existing property listing. Only the host (owner) can perform this action."
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a property",
        operation_description="Update one or more fields of an existing property listing. Only the host (owner) can perform this action."
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a property",
        operation_description="Delete an existing property listing. Only the host (owner) can perform this action."
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
