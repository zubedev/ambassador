from django.urls import path

from checkout import views

urlpatterns = [
    path('links/<str:code>/', views.LinkAPIView.as_view()),
]
