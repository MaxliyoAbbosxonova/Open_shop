from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.views import TokenViewBase

from users.serializers import SendSmsCodeSerializer, VerifySmsCodeSerializer
from users.utils import check_sms_code, random_code, send_sms_code


class CustomTokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    _serializer_class = api_settings.TOKEN_REFRESH_SERIALIZER
    authentication_classes = (JWTAuthentication,)


class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        phone = serializer.validated_data['phone']
        # send_sms_code(phone, code)
        result = send_sms_code(phone, code)

        if not result["allowed"]:
            return Response(
                {
                    "message": f"{result['remain_seconds']} sekunddan so'ng yubora olasiz."
                },
                status=429
            )
        return Response({"message": "send sms code"})


class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        is_valid_code = check_sms_code(phone, code)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)
