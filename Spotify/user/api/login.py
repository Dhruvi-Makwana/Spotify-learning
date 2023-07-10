from rest_framework.views import APIView
from user.serializers import LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth import login
from user.constants import LOGIN_VALIDATION_ERROR_MESSAGE


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        user = authenticate(request=request, **serializer.validated_data)
        if not user:
            raise ValidationError(LOGIN_VALIDATION_ERROR_MESSAGE)
        login(request, user)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh token": str(refresh),
                "access token": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
