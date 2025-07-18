from django.core.management.base import BaseCommand
from listings.models import Listing, User
import uuid
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **kwargs):
        host, created = User.objects.get_or_create(
            name='Coder',
            defaults={
                'first_name': 'Host',
                'last_name': 'User',
                'password': 'hashed_password',
            }
        )

        for i in range(10):
            Listing.objects.create(
                host=host,
                name=f"Listing {i + 1}",
                description="A lovely place to stay",
                location=random.choice(["New York", "London", "Paris", "Berlin", "Kigali"]),
                pricepernight=Decimal(str(random.randint(50, 300)))
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with listings.'))
