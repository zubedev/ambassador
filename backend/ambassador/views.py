from logging import getLogger

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics

from common.serializers import ProductSerializer
from core.models import Product

logger = getLogger(__name__)


class ProductFrontendView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    ordering = ('id',)  # default order

    @method_decorator(cache_page(15 * 60, key_prefix='products_frontend'))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, *kwargs)


class ProductBackendView(generics.ListAPIView):
    # queryset = Product.objects.all()  # overridden with get_queryset()
    serializer_class = ProductSerializer
    search_fields = ('title', 'description')
    ordering_fields = ('id', 'title', 'price')
    ordering = ('id', )  # default order

    def get_queryset(self):
        """Overridden to include redis caching"""
        qs = cache.get('products_backend')

        if not qs:  # no cache found
            qs = Product.objects.all()
            cache.set('products_backend', qs, timeout=15 * 60)  # 15 mins TTL

        return qs
