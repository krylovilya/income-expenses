from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     get_object_or_404)

from apps.users.serializers.serializer import (UserCreateSerializer,
                                               UserInfoSerializer)


class UserInfoView(RetrieveAPIView):
    """Получение информации о пользователе"""

    queryset = get_user_model().objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.request.user.pk)
        return obj


class UserRegistrationView(CreateAPIView):
    """Регистрация пользователя"""

    queryset = get_user_model().objects.all()
    serializer_class = UserCreateSerializer
