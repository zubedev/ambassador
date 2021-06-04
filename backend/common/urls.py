from django.urls import path

from backend.common import views

urlpatterns = [
    # auth
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    # user
    path('user/', views.UserAPIView.as_view(), name='user'),
    path('user/update/', views.UserUpdateAPIView.as_view(), name='user_update'),
    path('user/passwd/', views.UserPasswordAPIView.as_view(), name='user_passwd'),
]
