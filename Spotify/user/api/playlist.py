from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from user.serializers import PlaylistSerializer, GetPlaylistSerializer
from user.models import User, Song, Playlist
from django.db.models import Q
from user.choice import PRIVATE, COMMUNITY, PUBLIC
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated

READONLY = ["GET"]


class AdminOrUser(BasePermission):
    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        if request.method in READONLY:
            return is_authenticated
        return is_authenticated and request.user.is_staff


class PlaylistAPI(ListCreateAPIView):
    serializer_class = GetPlaylistSerializer
    permission_classes = [AdminOrUser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Playlist.objects.filter(
                Q(owned_by__id=self.request.user.id)
                | Q(privacy__in=[PRIVATE, COMMUNITY, PUBLIC])
            )
        return Playlist.objects.filter(privacy=PUBLIC)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PlaylistSerializer
        return super().get_serializer_class()


class UpdatePlayListAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = PlaylistSerializer
    permission_classes = [AdminOrUser]

    def get_queryset(self):
        return Playlist.objects.filter(Q(owned_by__id=self.request.user.id))
