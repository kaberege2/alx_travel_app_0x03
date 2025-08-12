from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from .permissions import IsAuthenticatedIsOwnerOrReadOnlyListing, IsAuthenticatedIsOwnerBooking
from django.contrib.auth import get_user_model
from .serializers import BookingSerializer, ListingSerializer, PaymentSerializ
from drf_yasg.utils import swagger_auto_schema
from .models import Booking, Listing
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import StandardResultsSetPagination
import uuid, requests, os
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Payment, Booking
from .serializers import PaymentSerializer

CHAPA_SECRET_KEY = os.environ.get('CHAPA_SECRET_KEY')

User = get_user_model()  # Custom user model

# Booking view
class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticatedIsOwnerBooking]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["property", "start_date", "end_date", "total_price", "status", "created_at"]
    search_fields = ["property", "start_date", "end_date", "total_price", "status", "created_at"]
    ordering_fields = ["property", "start_date", "end_date", "total_price", "status", "created_at"]
    odering = ["property"]

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
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "description", "location", "pricepernight", "created_at"]
    search_fields =  ["name", "description", "location", "pricepernight", "created_at"]
    ordering_fields =  ["name", "description", "location", "pricepernight", "created_at"]
    odering = ["name"]

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

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='initiate')
    def initiate_payment(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found or not yours'}, status=status.HTTP_404_NOT_FOUND)

        tx_ref = f"{uuid.uuid4()}"
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            tx_ref=tx_ref
        )

        payload = {
            "amount": str(payment.amount),
            "currency": "ETB",
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "tx_ref": tx_ref,
            "callback_url": "https://yourdomain.com/api/payments/callback/",
            "return_url": "https://yourdomain.com/payment-success/",
            "customization": {
                "title": "Booking Payment",
                "description": f"Payment for booking {booking.booking_id}"
            }
        }

        headers = {
            "Authorization": f"Bearer {CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        chapa_response = requests.post(
            "https://api.chapa.co/v1/transaction/initialize",
            json=payload,
            headers=headers
        )

        data = chapa_response.json()
        if chapa_response.status_code == 200 and data.get('status') == 'success':
            return Response({
                "checkout_url": data['data']['checkout_url'],
                "tx_ref": tx_ref
            })
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='verify/(?P<tx_ref>[^/.]+)')
    def verify_payment(self, request, tx_ref=None):
        try:
            payment = Payment.objects.get(tx_ref=tx_ref, booking__user=request.user)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
        response = requests.get(
            f"https://api.chapa.co/v1/transaction/verify/{tx_ref}",
            headers=headers
        )

        data = response.json()
        if data.get('status') == 'success':
            chapa_status = data['data']['status']
            payment.status = 'completed' if chapa_status == 'success' else 'failed'
            payment.chapa_transaction_id = data['data']['reference']
            payment.save()
            return Response({"status": payment.status, "chapa_response": data})
        else:
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
