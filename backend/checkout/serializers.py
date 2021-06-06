from rest_framework import serializers

from common.serializers import UserSerializer, ProductSerializer
from core.models import Link


class LinkSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Link
        fields = '__all__'
