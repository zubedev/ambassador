from decimal import Decimal
from random import randrange

from django.core.management import BaseCommand
from django.utils.crypto import get_random_string
from faker import Faker

from core.models import User, Order, OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        # get the ambassadors
        ambassadors = User.objects.filter(is_ambassador=True)

        for amb in ambassadors:  # for each ambassador

            # create orders for each ambassador
            for _ in range(randrange(1, 5)):
                order = Order.objects.create(
                    user=amb,  # ambassador
                    code=get_random_string(15),
                    amb_email=amb.email,
                    first_name=faker.first_name(),
                    last_name=faker.last_name(),
                    email=faker.email(),
                    is_complete=True)

                # populate each order with items
                for _ in range(randrange(1, 5)):
                    price = faker.pydecimal(2, 2, True, 1, 99)
                    quant = randrange(1, 5)
                    OrderItem.objects.create(
                        order=order,  # order
                        title=faker.bs(),
                        price=price,
                        quantity=quant,
                        admin_revenue=Decimal(0.9) * price * quant,
                        ambassador_revenue=Decimal(0.1) * price * quant)
