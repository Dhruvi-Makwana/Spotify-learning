from rest_framework.generics import RetrieveAPIView
from user.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated


class ProfileAPI(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
