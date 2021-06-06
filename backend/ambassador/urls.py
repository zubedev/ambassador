from django.urls import path, include

from ambassador import views

urlpatterns = [
    path('', include('common.urls')),

    path('products/frontend/', views.ProductFrontendView.as_view(), name='products_frontend'),
    path('products/backend/', views.ProductBackendView.as_view(), name='products_backend'),
    path('links/', views.LinkCreateListView.as_view(), name='links'),
]
