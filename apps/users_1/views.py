from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users_1.serializers import SendSmsCodeSerializer, VerifySmsCodeSerializer
from users_1.utils import random_code, send_sms_code, check_sms_code


class SendCodeAPIView(APIView):
    serializers_class=SendSmsCodeSerializer
    def post(self, request):
        serializer = SendSmsCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code=random_code()
        phone=serializer.validated_data['phone']
        send_sms_code(phone, code)
        return Response({"message":"send sms code"})


class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifySmsCodeSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)

        return Response(serializer.get_data)