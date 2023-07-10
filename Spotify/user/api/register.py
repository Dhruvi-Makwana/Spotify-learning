from rest_framework.views import APIView
from user.serializers import UserSerializer
from rest_framework.generics import CreateAPIView
from user.models import User


class RegistrationAPI(CreateAPIView):
    queryset = User.objects.none()
    serializer_class = UserSerializer
