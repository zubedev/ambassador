import random
import string
from logging import getLogger

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.auth import JWTAuth
from common.serializers import ProductSerializer, LinkSerializer
from core.models import Product, Link

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


class LinkCreateListView(generics.ListCreateAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    ordering = ('id', )

    def create(self, request, *args, **kwargs):
        # add the user and code
        request.data.update({
            'user': request.user.id,
            'code': ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        })

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Link.objects.filter(user=self.request.user)


class RankingsAPIView(APIView):
    authentication_classes = [JWTAuth]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        conn = get_redis_connection('default')

        # https://redis.io/commands/zrevrangebyscore
        rankings = conn.zrevrangebyscore('rankings', min=0, max=1000, withscores=True)

        rankings = {rank[0].decode('utf-8'): rank[1] for rank in rankings}

        return Response(rankings)
