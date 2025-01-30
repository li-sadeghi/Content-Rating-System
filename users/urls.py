from django.urls import path

from rest_framework_simplejwt import views as jwt_views
from users import views as users_views

urlpatterns = [
    path("register/", users_views.UserRegistrationView.as_view(), name="auth_register"),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh_token/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
