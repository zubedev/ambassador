from django.core.management import BaseCommand
from faker import Faker

from core.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        products = []  # for bulk create

        for _ in range(90):
            prod = Product(
                title=faker.company(),
                description=faker.text(200),
                image=faker.image_url(),
                price=faker.pydecimal(3, 2, True, 1, 999))
            products.append(prod)

        Product.objects.bulk_create(products)
