from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserInfoSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """Для хеширования пароля"""

        user = self.Meta.model(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
