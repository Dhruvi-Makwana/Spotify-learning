from .models import User, Song, Playlist
from rest_framework import serializers
from .constants import PASSWORD_ERROR_MESSAGE
from django.contrib.auth.models import Group
from rest_framework.serializers import ValidationError
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "groups",
            "profile_photo",
            "password",
            "confirm_password",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if not password == confirm_password:
            raise serializers.ValidationError("password does not match")
        attrs.pop("confirm_password", None)
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=False)


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "groups",
            "profile_photo",
            "full_name",
        )


class CreateSongSerializer(serializers.ModelSerializer):
    def validate_play_song(self, value):
        if value:
            if not value.name.endswith(".mp3"):
                raise ValidationError("Only .mp3 files are allowed.")
        return value

    class Meta:
        model = Song
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    singer = UserSerializer(read_only=True)
    written_by = UserSerializer(read_only=True)

    class Meta:
        model = Song
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = "__all__"


class GetPlaylistSerializer(serializers.ModelSerializer):
    song = CreateSongSerializer(many=True)
    owned_by = UserSerializer(read_only=True)

    class Meta:
        model = Playlist
        fields = (
            "id",
            "name",
            "owned_by",
            "song",
            "privacy",
        )
