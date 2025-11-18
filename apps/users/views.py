from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import SendSmsCodeSerializer, VerifySmsCodeSerializer
from users.utils import SMSRateThrottle, check_sms_code, random_code, send_sms_code


class SendCodeAPIView(APIView):
    serializer_class = SendSmsCodeSerializer
    throttle_classes = [SMSRateThrottle]
    throttle_scope = 'sms'

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = random_code()
        print(code)
        phone = serializer.validated_data['phone']
        send_sms_code(phone, code)
        return Response({"message": "send sms code"})


class LoginAPIView(APIView):
    serializer_class = VerifySmsCodeSerializer

    def post(self, request, *args, **kwargs):
        try:
            self.check_throttles(request)
        except Exception as e:
            return Response(
                {"error": " 1 daqiqada faqat 1 marta SMS yuborishingiz mumkin. Iltimos kuting."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        is_valid_code = check_sms_code(**serializer.data)
        if not is_valid_code:
            return Response({"message": "invalid code"}, status.HTTP_400_BAD_REQUEST)
        # token generate
        return Response(serializer.data)
