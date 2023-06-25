from rest_framework.generics import RetrieveUpdateAPIView
from users.serializers import UserProfileSerializer


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
