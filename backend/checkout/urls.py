from django.urls import path

from checkout import views

urlpatterns = [
    path('links/<str:code>/', views.LinkRetrieveAPIView.as_view()),
    path('orders/', views.OrderCreateAPIView.as_view()),
]
