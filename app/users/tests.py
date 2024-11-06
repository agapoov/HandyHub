from django.test import TestCase
from django.urls import reverse
from .models import User
from http import HTTPStatus


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.data = {
            'username': 'TestUsername',
            'email': 'example@gmail.com',
            'first_name': 'TestFirstName',
            'last_name': 'TestLastName',
            'surname': 'TestSurname',
            'password1': 'SomePass1234',
            'password2': 'SomePass1234'
        }
        self.path = reverse('users:registration')

    def test_registration_get(self):
        """Test the registration view"""
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_successful_registration(self):
        """Test that user registration works"""
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

    def test_password_missmatch(self):
        """Test password missmatch"""
        self.data['password2'] = 'Different Password'
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_already_exists(self):
        """Test user already exists"""
        User.objects.create_user(
            username='TestUsername',  # same that in self.data
            email='example@mail.ru',
            password='Password123123'
        )
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
