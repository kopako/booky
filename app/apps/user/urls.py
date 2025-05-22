from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views.user import LogOutAPIView, RegisterUserAPIView, LogInAPIView

app_name = "user"



urlpatterns = [
                  path('auth-login/', LogInAPIView.as_view()),
                  path('auth-logout/', LogOutAPIView.as_view()),
                  path('auth-register/', RegisterUserAPIView.as_view()),
                  path('auth-login-jwt/', TokenObtainPairView.as_view()),
                  path('token-refresh/', TokenRefreshView.as_view()),
    ]