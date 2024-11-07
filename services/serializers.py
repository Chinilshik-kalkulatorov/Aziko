from rest_framework import serializers
from .models import User, UserProfile 
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.

    Проверяет корректность введённых данных и создаёт новый профиль пользователя.
    """
    name = serializers.CharField(
        max_length=100,
        help_text="Имя пользователя (только латинские буквы и пробелы)"
    )
    phone_number = serializers.CharField(
        max_length=15,
        help_text="Номер телефона в формате '+1234567890'"
    )

    class Meta:
        model = UserProfile
        fields = ['name', 'phone_number']

    def validate_name(self, value):
        value = value.lower()
        if not re.fullmatch(r'[a-zA-Z ]+', value):
            raise serializers.ValidationError("Name must contain only Latin letters and spaces")
        return value

    def validate_phone_number(self, value):
        # Проверяем, что номер телефона содержит только цифры и '+' в начале (опционально)
        if not re.fullmatch(r'^\+?\d{7,15}$', value):
            raise serializers.ValidationError("Invalid phone number format")
        return value

class PhoneVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    verification_code = serializers.CharField(max_length=6)

    def validate(self, data):
        phone_number = data.get('phone_number')
        verification_code = data.get('verification_code')

        try:
            user = UserProfile.objects.get(phone_number=phone_number)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("Phone number not found")

        if user.verification_code != verification_code:
            raise serializers.ValidationError("Invalid verification code")

        return data
