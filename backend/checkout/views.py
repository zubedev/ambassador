from logging import getLogger

import stripe
from django.core.mail import send_mail
from django.db import transaction
from rest_framework import generics, exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.serializers import OrderSerializer
from .serializers import LinkSerializer
from core.models import Link, Order

logger = getLogger(__name__)


class LinkRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    lookup_field = 'code'


class OrderCreateAPIView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            link = Link.objects.get(code=request.data.get('code'))
            request.data.update({
                'user_id': link.user.pk,
                'amb_email': link.user.email})
            return super().post(request, *args, **kwargs)
        except Link.DoesNotExist:
            raise exceptions.APIException('Invalid code!')
        except Exception as e:
            transaction.rollback()
            logger.error(e)
            raise exceptions.APIException('Something went wrong!')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = serializer.save()

        items = []
        for i in order.order_items.all():
            items.append({
                'name': i.title,
                'description': i.title,
                'images': [i.title],
                'amount': int(i.price * 100),  # cents
                'quantity': i.quantity,
                'currency': 'aud'})

        stripe.api_key = 'sk_test_51J11XRDEXObcVUNODQHKXJfqUkdMQDNz5doqvIf2tvYjYLqpfkXJ54LbON2ts0s9SX0JwjS6pFBl5KuCMy1P9Wim008FEjy4zK'
        source = stripe.checkout.Session.create(
            success_url='http://localhost:5000/success?source={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:5000/error',
            payment_method_types=['card'],
            line_items=items)

        order.trans_id = source['id']
        order.save()

        headers = self.get_success_headers(source)
        return Response(source, status=status.HTTP_201_CREATED, headers=headers)


class OrderConfirmAPIView(APIView):
    def post(self, request):
        order = Order.objects.filter(trans_id=request.data['source']).first()
        if not order:
            raise exceptions.APIException('Order not found!')

        order.is_complete = True
        order.save()

        send_mail(  # Admin email
            subject='An order has been completed',
            message=f'Order #{order.id} with a total of ${order.admin_revenue} has been completed!',
            from_email='noreply@email.com',
            recipient_list=['admin@email.com'])

        send_mail(  # Ambassador email
            subject='An order has been completed',
            message=f'You have earned ${order.ambassador_revenue} from the link #{order.code}',
            from_email='noreply@email.com',
            recipient_list=[order.amb_email])

        return Response({'message': 'success'})
