from logging import getLogger

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from common.serializers import UserSerializer

logger = getLogger(__name__)


class AmbassadorsAPIView(APIView):
    def get(self, _):
        amb = get_user_model().objects.filter(is_ambassador=True)
        ser = UserSerializer(amb, many=True)

        return Response(ser.data)
