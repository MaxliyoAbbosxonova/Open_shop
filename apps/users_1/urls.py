from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users_1.views import SendCodeAPIView, LoginAPIView

urlpatterns=[
    path('auth/send-code', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('auth/verify-code', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
]