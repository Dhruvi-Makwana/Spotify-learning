from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from user.serializers import CreateSongSerializer, SongSerializer
from user.models import User, Song
from rest_framework.permissions import BasePermission


class AdminOrUser(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_superuser
        elif request.method == "PATCH":
            return request.user.is_authenticated and request.user.is_staff
        return True


class SongAPI(ListCreateAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    permission_classes = [AdminOrUser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateSongSerializer
        return super().get_serializer_class()


class UpdateSongAPI(RetrieveUpdateDestroyAPIView):
    serializer_class = SongSerializer
    permission_classes = [AdminOrUser]

    def get_queryset(self):
        return Song.objects.all()
