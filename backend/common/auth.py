from logging import getLogger

from django.conf import settings
from django.utils import timezone

import jwt

logger = getLogger(__name__)


class JWTAuth:
    """JSON Web Token Authentication class"""

    @staticmethod
    def get_jwt(uid: int):
        """Generates JWT with given user ID"""
        payload = {
            "id": uid,  # user id
            "exp": timezone.now() + timezone.timedelta(minutes=15),  # expiry
            "iat": timezone.now()  # issued at
        }

        return jwt.encode(payload, settings.SECRET_KEY)  # algorithm = "HS256"
