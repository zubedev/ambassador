from django.core.management import BaseCommand
from django_redis import get_redis_connection

from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        conn = get_redis_connection('default')

        qs = User.objects.filter(is_ambassador=True)

        for obj in qs:
            # https://redis.io/commands/ZADD
            conn.zadd('rankings', {obj.name: float(obj.revenue)})
