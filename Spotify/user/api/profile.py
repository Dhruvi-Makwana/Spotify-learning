from rest_framework.views import APIView
from user.serializers import UserProfileSerializer
from user.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class ProfileAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        get_user_id = kwargs.get("pk")
        user_data = User.objects.filter(id=get_user_id)
        serializer = UserProfileSerializer(user_data, many=True)
        return JsonResponse({"data": serializer.data}, status=status.HTTP_200_OK)
