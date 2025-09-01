from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Patient, Doctor
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

    def test_authenticated_user_can_update_profile(self):
        """
        Ensure an authenticated user can update their own profile.
        """
        url = reverse('user-profile')
        updated_data = {
            'phone': '0987654321',
            'birthday': '1995-05-20'
        }
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh the user object from the database to get the updated values
        self.user.refresh_from_db()
        
        self.assertEqual(self.user.phone, updated_data['phone'])
        self.assertEqual(str(self.user.birthday), updated_data['birthday'])

class DoctorAPITest(APITestCase):
    def test_can_list_doctors(self):
        """
        Ensure API can list all available doctors.
        """
        # Create some doctors
        Doctor.objects.create(name='Dr. Emily Carter', specialty='Cardiology')
        Doctor.objects.create(name='Dr. Ben Adams', specialty='Neurology')

        url = reverse('doctor-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'Dr. Emily Carter')

    def test_can_retrieve_single_doctor(self):
        """
        Ensure API can retrieve a single doctor by their ID.
        """
        doctor = Doctor.objects.create(name='Dr. Gregory House', specialty='Diagnostic Medicine')
        
        url = reverse('doctor-detail', kwargs={'pk': doctor.pk})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], doctor.name)

