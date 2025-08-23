from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment

@shared_task
def send_payment_confirmation_email(user_email, payment_id):
    """
    Sends a confirmation email to the user after a successful payment.
    """
    try:
        payment = Payment.objects.get(payment_id=payment_id)
    except Payment.DoesNotExist:
        return f"Payment with ID {payment_id} not found"

    subject = "Payment Confirmation"
    message = (
        f"Hello {payment.booking.user.first_name},\n\n"
        f"Your payment for booking {payment.booking.booking_id} has been successfully processed.\n"
        f"Amount Paid: {payment.amount} USD'\n"
        f"Transaction Reference: {payment.tx_ref}\n"
        f"Chapa Transaction ID: {payment.chapa_transaction_id}\n\n"
        "Thank you for your payment!\n\n"
        "Best regards,\n"
        "Your Booking Team"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

    return f"Confirmation email sent to {user_email}"
