from django.urls import path

from user.api.register import RegistrationAPI
from user.api.login import LoginAPIView
from user.api.profile import ProfileAPI
from user.api.song import SongAPI, UpdateSongAPI
from user.api.playlist import PlaylistAPI, UpdatePlayListAPI
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = "user"
urlpatterns = [
    path("api/register/", RegistrationAPI.as_view(), name="register-api"),
    path("api/profile/", ProfileAPI.as_view(), name="profile-api"),
    path(
        "api/login/",
        LoginAPIView.as_view(),
        name="loginAPI",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/song/", SongAPI.as_view(), name="song-api"),
    path("api/song/<int:pk>", UpdateSongAPI.as_view(), name="update-song-api"),
    path("api/playlist/", PlaylistAPI.as_view(), name="playlist-api"),
    path(
        "api/playlist/<int:pk>", UpdatePlayListAPI.as_view(), name="update-playlist-api"
    ),
]
