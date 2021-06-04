from logging import getLogger

from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .auth import JWTAuth
from .serializers import UserSerializer

logger = getLogger(__name__)


class RegisterAPIView(APIView):
    permission_classes = (AllowAny,)  # override default: IsAuthenticated

    def post(self, request):
        """POST method for Register"""
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


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )  # override default: IsAuthenticated

    def post(self, request):
        """POST method for Login"""
        data: dict = request.data
        # get the user
        user = get_user_model().objects.filter(email=data.get('email')).first()
        # check if user exists
        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')
        # check for correct password
        if not user.check_password(data.get('password')):
            raise exceptions.AuthenticationFailed('Incorrect password!')
        # get jwt
        jwt = JWTAuth.get_jwt(user.id)
        # set cookie
        res = Response()
        res.set_cookie('jwt', jwt, httponly=True)
        res.data = {'message': 'success'}

        return res


class UserAPIView(APIView):
    # authentication_classes = (JWTAuth, )  # set as default in settings
    # permission_classes = (IsAuthenticated, )  # set as default in settings

    def get(self, request):
        """GET method for User Info API"""
        return Response(UserSerializer(request.user).data)
