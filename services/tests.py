from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Username, UserProfile
from unittest.mock import patch

class UsernameValidationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_username = 'JohnDoe'
        self.url = reverse('server_name', args=[self.valid_username])

        # Добавляем имя в базу данных
        Username.objects.create(name=self.valid_username)

    def test_validate_username_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.valid_username.lower())

    def test_validate_username_invalid_characters(self):
        invalid_username = 'John_Doe!'
        url = reverse('server_name', args=[invalid_username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username must contain only Latin letters')

    def test_validate_username_not_found(self):
        non_existing_username = 'NonExistingUser'
        url = reverse('server_name', args=[non_existing_username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No such name')


class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register_user')
        self.valid_data = {
            'name': 'Jane Doe',
            'phone_number': '+1234567890'
        }

    @patch('services.views.send_sms')
    def test_user_registration_success(self, mock_send_sms):
        response = self.client.post(self.register_url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Verification code sent to your phone')

        # Проверяем, что пользователь создан в базе данных
        user = UserProfile.objects.get(phone_number=self.valid_data['phone_number'])
        self.assertEqual(user.name, self.valid_data['name'].lower())
        self.assertFalse(user.is_verified)
        self.assertIsNotNone(user.verification_code)

        # Проверяем, что функция отправки SMS была вызвана
        mock_send_sms.assert_called_once_with(user.phone_number, user.verification_code)

    def test_user_registration_invalid_name(self):
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = 'ИмяНаКириллице'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_user_registration_invalid_phone(self):
        invalid_data = self.valid_data.copy()
        invalid_data['phone_number'] = 'invalid_phone'
        response = self.client.post(self.register_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)


class PhoneVerificationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.verify_url = reverse('verify_phone')
        self.user = UserProfile.objects.create(
            name='jane doe',
            phone_number='+1234567890',
            is_verified=False,
            verification_code='123456'
        )

    def test_phone_verification_success(self):
        data = {
            'phone_number': self.user.phone_number,
            'verification_code': self.user.verification_code
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Phone number verified successfully')

        # Обновляем данные пользователя из базы данных
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        self.assertIsNone(self.user.verification_code)

    def test_phone_verification_wrong_code(self):
        data = {
            'phone_number': self.user.phone_number,
            'verification_code': '654321'  # Неверный код
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Invalid verification code')

    def test_phone_verification_non_existing_phone(self):
        data = {
            'phone_number': '+0987654321',  # Номер, не существующий в базе данных
            'verification_code': '123456'
        }
        response = self.client.post(self.verify_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertEqual(response.data['non_field_errors'][0], 'Phone number not found')
