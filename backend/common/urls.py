from django.urls import path

from backend.common import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]
