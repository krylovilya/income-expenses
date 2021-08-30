from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from apps.users.views.views import UserInfoView, UserRegistrationView

urlpatterns = [
    path('me/', UserInfoView.as_view(), name='user_info'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
