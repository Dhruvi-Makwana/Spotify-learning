from .models import User
from rest_framework import serializers
from .constants import PASSWORD_ERROR_MESSAGE
from user.utils import assign_role_to_user
from django.contrib.auth.models import Group


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
