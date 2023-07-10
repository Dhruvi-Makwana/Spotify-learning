from django.urls import path
from user.api.register import RegistrationAPI
from user.api.login import LoginAPIView
from user.api.profile import ProfileAPI
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = "user"
urlpatterns = [
    path("api/register/", RegistrationAPI.as_view(), name="registerAPI"),
    path("api/profile/<int:pk>", ProfileAPI.as_view(), name="profileAPI"),
    path(
        "api/login/",
        LoginAPIView.as_view(),
        name="loginAPI",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
