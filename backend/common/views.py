from logging import getLogger

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

logger = getLogger(__name__)


class RegisterAPIView(APIView):

    def post(self, request):
        """POST method"""
        data: dict = request.data

        # check if passwords match
        if data.get('password') != data.get('password_confirm'):
            raise exceptions.APIException('Passwords do not match!')

        # set is_ambassador attribute
        data.update({'is_ambassador': 0})

        # serialize the data
        ser = UserSerializer(data=data)
        ser.is_valid(raise_exception=True)  # raises ValidationError
        ser.save()

        return Response(data=ser.data)
