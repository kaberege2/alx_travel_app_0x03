import uuid
import random
from decimal import Decimal
from datetime import timedelta, date

from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from users.models import User
from listings.models import Listing, Booking

class Command(BaseCommand):
    help = "Seed the database with users, listings, and bookings"

    def handle(self, *args, **options):
        try:
            self.seed_users()
            self.seed_listings()
            self.seed_bookings()
            self.stdout.write(self.style.SUCCESS("Database successfully seeded."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Seeding failed: {str(e)}"))

    def seed_users(self):
        self.stdout.write("Seeding users...")

        self.hosts = []
        self.guests = []

        user_data = [
            {"email": "host1@example.com", "role": "host"},
            {"email": "host2@example.com", "role": "host"},
            {"email": "guest1@example.com", "role": "guest"},
            {"email": "guest2@example.com", "role": "guest"},
            {"email": "admin@example.com", "role": "admin"},
        ]

        for data in user_data:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "first_name": data["email"].split("@")[0].capitalize(),
                    "last_name": "User",
                    "phone_number": "123456789",
                    "role": data["role"],
                    "password": "hashed",  # `set_password` not needed unless used for login
                }
            )
            if data["role"] == "host":
                self.hosts.append(user)
            elif data["role"] == "guest":
                self.guests.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(user_data)} users."))

    def seed_listings(self):
        self.stdout.write("Seeding listings...")

        self.listings = []
        locations = ["Kigali", "Paris", "New York", "London", "Berlin"]

        for host in self.hosts:
            for i in range(2):  # each host gets 2 listings
                try:
                    with transaction.atomic():
                        listing = Listing.objects.create(
                            host=host,
                            name=f"{host.first_name}'s Listing {i + 1}",
                            description="A cozy and comfortable place to stay.",
                            location=random.choice(locations),
                            pricepernight=Decimal(random.randint(50, 300)),
                        )
                        self.listings.append(listing)
                except IntegrityError as e:
                    self.stderr.write(self.style.ERROR(f"Error creating listing: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Created {len(self.listings)} listings."))

    def seed_bookings(self):
        self.stdout.write("Seeding bookings...")

        status_choices = ["pending", "confirmed", "canceled"]

        for guest in self.guests:
            booked_listings = random.sample(self.listings, k=2)

            for listing in booked_listings:
                try:
                    start = date.today() + timedelta(days=random.randint(1, 30))
                    end = start + timedelta(days=random.randint(1, 7))
                    total_days = (end - start).days
                    total_price = total_days * listing.pricepernight

                    with transaction.atomic():
                        Booking.objects.create(
                            user=guest,
                            property=listing,
                            start_date=start,
                            end_date=end,
                            total_price=total_price,
                            status=random.choice(status_choices),
                        )
                except IntegrityError as e:
                    self.stderr.write(self.style.ERROR(f"Error creating booking: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Created bookings for guests."))
