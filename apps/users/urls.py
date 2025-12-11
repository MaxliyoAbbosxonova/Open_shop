from django.urls import path

from users.views import CustomTokenRefreshView, LoginAPIView, SendCodeAPIView

urlpatterns = [
    path('send-code/', SendCodeAPIView.as_view(), name='token_obtain_pair'),
    path('verify-code/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
