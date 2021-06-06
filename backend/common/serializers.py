from logging import getLogger

from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Product, Link, Order

logger = getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    revenue = serializers.SerializerMethodField('get_revenue')

    class Meta:
        model = get_user_model()
        fields = '__all__'
        read_only_fields = (
            'last_login', 'date_joined', 'groups', 'user_permissions',
            'is_active', 'is_staff', 'is_superuser', 'is_ambassador')
        extra_kwargs = {
            'password': {
                'write_only': True,  # does not expose field in GET
                'min_length': 8,  # minimum length of password
                'style': {'input_type': 'password'},  # for browsable API
        }}

    def get_revenue(self, obj):
        return obj.revenue

    def create(self, validated_data):
        """Overriding to handle with custom user manager"""
        logger.debug(
            f"Creating user: email={validated_data.get('email', None)}")
        return self.Meta.model.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(method_name='get_count')
    revenue = serializers.SerializerMethodField(method_name='get_revenue')

    class Meta:
        model = Link
        fields = '__all__'

    def get_count(self, obj):
        return Order.objects.filter(code=obj.code, is_complete=True).count()

    def get_revenue(self, obj):
        orders = Order.objects.filter(code=obj.code, is_complete=True)
        return sum(o.ambassador_revenue for o in orders)
