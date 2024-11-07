from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User, Username, UserProfile
from .utils import send_sms
from .serializers import UserSerializer, UserRegistrationSerializer, PhoneVerificationSerializer

import re 
import random

def registration_page(request):
    return render(request, 'services/register.html')

def verification_page(request):
    return render(request, 'services/verify_phone.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def server_name(request, username=None):
    if request.method == 'POST':
        username = request.data.get('username')

    if not username:
        return Response({"error": "Username not provided"}, status=status.HTTP_400_BAD_REQUEST)

    username = username.lower()  # Преобразуем имя в нижний регистр

    # Проверяем, что имя содержит только латинские буквы
    if not re.fullmatch(r'[a-zA-Z]+', username):
        return Response({"error": "Username must contain only Latin letters"}, status=status.HTTP_400_BAD_REQUEST)

    # Проверяем существование имени в базе данных
    if Username.objects.filter(name=username).exists():
        return Response({"username": username}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "No such name"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        phone_number = serializer.validated_data['phone_number']
        verification_code = str(random.randint(100000, 999999))

        user, created = UserProfile.objects.update_or_create(
            phone_number=phone_number,
            defaults={
                'name': name,
                'verification_code': verification_code,
                'is_verified': False,
            }
        )

        send_sms(phone_number, verification_code)

        print(f"Verification code for {phone_number}: {verification_code}")  # Для отладки

        return Response({"message": "Verification code sent to your phone"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_phone(request):
    serializer = PhoneVerificationSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']

        user = UserProfile.objects.get(phone_number=phone_number)
        user.is_verified = True
        user.verification_code = None
        user.save()

        return Response({"message": "Phone number verified successfully"}, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
