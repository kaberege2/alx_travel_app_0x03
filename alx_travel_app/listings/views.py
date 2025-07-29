from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import BookingSerializer, ListingSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Booking, Listing

User = get_user_model()  # Custom user model

class BookingViewSet(viewsets.ModelViewSet):
    queryset=Booking.objects.all()
    serializer_class=BookingSerializer
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all jobs created by the recruiter.",
        operation_summary="List Jobs"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new job.",
        operation_summary="Create Job"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a job by ID.",
        operation_summary="Retrieve Job"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a job posting.",
        operation_summary="Update Job"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a job posting.",
        operation_summary="Partial Update Job"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a job posting.",
        operation_summary="Delete Job"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ListingViewSet(viewsets.ModelViewSet):
    queryset=Listing.objects.all()
    serializer_class=ListingSerializer
    permission_classes=[IsAuthenticated]

    @swagger_auto_schema(
        operation_description="List all jobs created by the recruiter.",
        operation_summary="List Jobs"
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new job.",
        operation_summary="Create Job"
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a job by ID.",
        operation_summary="Retrieve Job"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a job posting.",
        operation_summary="Update Job"
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a job posting.",
        operation_summary="Partial Update Job"
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a job posting.",
        operation_summary="Delete Job"
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    