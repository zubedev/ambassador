from rest_framework import serializers

from core.models import Product, Link, OrderItem, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField('get_total')

    def get_total(self, obj):
        model = self.order_items.Meta.model
        items = model.objects.filter(order_id=obj.id)
        return sum((i.price * i.quantity) for i in items)

    class Meta:
        model = Order
        fields = '__all__'