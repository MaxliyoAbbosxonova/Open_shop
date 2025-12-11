from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import LoginAPIView, SendCodeAPIView, CustomTokenRefreshView

urlpatterns = [
    path('send-code/', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('verify-code/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
