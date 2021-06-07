from decimal import Decimal
from logging import getLogger

from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Product, Link, Order, OrderItem

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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, required=False)
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('order_items', )

    def get_total(self, obj):
        items = OrderItem.objects.filter(order_id=obj.id)
        return sum((i.price * i.quantity) for i in items)

    def create(self, validated_data):
        request = self.context.get('request')
        products = request.data.get('products', None)

        order = super().create(validated_data)
        order.user_id = request.data.get('user_id')
        order.save()

        if products:
            self.handle_products(order, products)

        return order

    def handle_products(self, order: Order, products: list):
        order_items = []

        for item in products:
            product = Product.objects.get(id=item.get('product_id'))

            order_items.append(OrderItem(
                order_id=order.id,
                title=product.title,
                price=product.price,
                quantity=item.get('quantity'),
                admin_revenue=Decimal(0.9) * product.price * Decimal(item.get('quantity')),
                ambassador_revenue=Decimal(0.1) * product.price * Decimal(item.get('quantity')),
            ))

        OrderItem.objects.bulk_create(order_items)
