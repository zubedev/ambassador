from django.core.management import BaseCommand
from faker import Faker

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()
        ambassadors = []  # for bulk create

        for _ in range(30):
            user = User(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email())
            user.set_password(  # FirstLast
                f'{user.first_name.capitalize()}{user.last_name.capitalize()}')
            ambassadors.append(user)

        User.objects.bulk_create(ambassadors)
