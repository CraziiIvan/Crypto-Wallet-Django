from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, OTP

class RequestOTPAPI(APIView):
    
    @swagger_auto_schema(
        operation_description="Request an OTP for password reset",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
            },
        ),
        responses={
            200: openapi.Response(description='OTP sent to your email'),
            404: openapi.Response(description='User with this email does not exist'),
        },
    )
    def post(self, request):
        email = request.data.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        otp_obj, created = OTP.objects.get_or_create(user=user)
        otp = otp_obj.get_token()

        subject = 'OneStep OTP for Password Reset'
        message = f'Your password reset OTP code is:<br> <h2><strong>{otp}</strong></h2>'
        from_email = 'kyawkokotunmm475157@gmail.com'
        recipient_list = [email]

        send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, fail_silently=True, html_message=message, message='')

        return Response({'message': 'OTP sent to your email'}, status=status.HTTP_200_OK)


class ResetPasswordAPI(APIView):

    @swagger_auto_schema(
        operation_description="Reset password using OTP",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'otp', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING, description='OTP'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='New password'),
            },
        ),
        responses={
            200: openapi.Response(description='Password reset successful'),
            400: openapi.Response(description='Invalid OTP'),
            404: openapi.Response(description='User with this email does not exist'),
        },
    )
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        otp_obj = OTP.objects.get(user=user)

        if not otp_obj.verify(otp):
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
