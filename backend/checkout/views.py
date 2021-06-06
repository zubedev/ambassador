from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LinkSerializer
from core.models import Link


class LinkAPIView(APIView):

    def get(self, _, code=''):
        obj = Link.objects.get(code=code)
        ser = LinkSerializer(obj)

        return Response(ser.data)
