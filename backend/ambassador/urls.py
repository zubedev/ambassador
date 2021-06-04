from django.urls import path, include

# from ambassador import views

urlpatterns = [
    path('', include('common.urls')),
]
