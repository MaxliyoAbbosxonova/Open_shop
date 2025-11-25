import time

import redis
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import SendSmsCodeSerializer, VerifySmsCodeSerializer
from users.utils import check_sms_code, random_code, send_sms_code, _get_login_key

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        phone = serializer.validated_data['phone']
        send_sms_code(phone, code)
        return Response({"message": "send sms code"})


class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']
        code = serializer.validated_data['code']
        is_valid_code = check_sms_code(phone, code)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)
