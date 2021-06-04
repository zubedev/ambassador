from django.urls import path, include
from rest_framework.routers import DefaultRouter

from administrator import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('orders', views.OrderViewSet)

urlpatterns = [
    path('', include('common.urls')),
    path('', include(router.urls)),

    path('ambassadors/', views.AmbassadorsAPIView.as_view(), name='ambassadors'),
    path('users/<int:pk>/links/', views.LinksAPIView.as_view(), name='links'),
]
