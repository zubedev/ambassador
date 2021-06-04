from django.urls import path, include

from administrator import views

urlpatterns = [
    path('', include('common.urls')),

    path('ambassadors/', views.AmbassadorsAPIView.as_view(), name='ambassadors'),
]
