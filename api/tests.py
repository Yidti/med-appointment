from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Patient
from rest_framework.authtoken.models import Token

class RegistrationAPITest(APITestCase):
    def test_patient_can_register(self):
        """
        Ensure a new patient can register.
        """
        url = reverse('register')
        data = {
            "username": "testpatient",
            "email": "test.patient@example.com",
            "password": "someStrongPassword123",
            "phone": "1234567890",
            "birthday": "2000-01-01"
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 1)
        self.assertEqual(Patient.objects.get().email, 'test.patient@example.com')

class LoginAPITest(APITestCase):
    def setUp(self):
        self.email = "test.patient@example.com"
        self.password = "someStrongPassword123"
        self.user = Patient.objects.create_user(
            username="testloginuser", 
            email=self.email, 
            password=self.password
        )

    def test_patient_can_log_in(self):
        """
        Ensure an existing patient can log in and receive a token.
        """
        url = reverse('login')
        data = {
            "email": self.email,
            "password": self.password
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

class UserProfileAPITest(APITestCase):
    def setUp(self):
        self.user = Patient.objects.create_user(username='testprofileuser', email='test.profile@example.com', password='password123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_authenticated_user_can_get_profile(self):
        """
        Ensure an authenticated user can retrieve their own profile.
        """
        url = reverse('user-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)

    def test_unauthenticated_user_cannot_get_profile(self):
        """
        Ensure an unauthenticated user receives a 401 Unauthorized response.
        """
        self.client.credentials() # Clear credentials
        url = reverse('user-profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

