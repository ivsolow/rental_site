from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import CustomUser


User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'password', 'confirm_password')

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.pop('confirm_password', None)

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают.")

        return attrs


class UserLoginSerializer(BaseUserRegistrationSerializer):

    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ('email', 'password', )


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'date_of_birth']
