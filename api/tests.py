from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Patient, Doctor, Schedule, Appointment
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

class ScheduleAPITest(APITestCase):
    def setUp(self):
        self.doctor1 = Doctor.objects.create(name='Dr. Alan Grant', specialty='Paleontology')
        self.doctor2 = Doctor.objects.create(name='Dr. Ellie Sattler', specialty='Paleobotany')

        # Schedules for Doctor 1
        self.schedule1 = Schedule.objects.create(doctor=self.doctor1, date='2025-10-20', start_time='09:00', end_time='09:30', is_available=True)
        self.schedule2 = Schedule.objects.create(doctor=self.doctor1, date='2025-10-20', start_time='10:00', end_time='10:30', is_available=False)
        self.schedule3 = Schedule.objects.create(doctor=self.doctor1, date='2025-10-21', start_time='09:00', end_time='09:30', is_available=True)

        # Schedule for Doctor 2
        self.schedule4 = Schedule.objects.create(doctor=self.doctor2, date='2025-10-20', start_time='14:00', end_time='14:30', is_available=True)

    def test_can_list_schedules_for_a_specific_doctor_on_a_specific_date(self):
        """
        Ensure API returns only the schedules for the given doctor and date.
        """
        url = f"{reverse('schedule-list')}?doctor_id={self.doctor1.pk}&date=2025-10-20"
        
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Should only return schedule1 and schedule2
        # Check if the returned schedules belong to the correct doctor and date
        for schedule_data in response.data:
            self.assertEqual(schedule_data['doctor'], self.doctor1.pk)


class AppointmentAPITest(APITestCase):
    def setUp(self):
        self.patient1 = Patient.objects.create_user(username='patient1', email='patient1@example.com', password='password123')
        self.token1 = Token.objects.create(user=self.patient1)

        self.patient2 = Patient.objects.create_user(username='patient2', email='patient2@example.com', password='password456')
        self.token2 = Token.objects.create(user=self.patient2)

        self.doctor = Doctor.objects.create(name='Dr. Who', specialty='Time Lord')
        self.available_schedule = Schedule.objects.create(doctor=self.doctor, date='2025-12-25', start_time='10:00', end_time='10:30', is_available=True)
        self.unavailable_schedule = Schedule.objects.create(doctor=self.doctor, date='2025-12-26', start_time='11:00', end_time='11:30', is_available=False)

        # Patient 1 has an appointment
        self.appointment1 = Appointment.objects.create(patient=self.patient1, schedule=self.available_schedule, status='booked')
        # This schedule should now be unavailable, let's reflect that for correctness in tests
        self.available_schedule.is_available = False
        self.available_schedule.save()

    def test_patient_can_create_appointment_for_available_schedule(self):
        """
        Ensure an authenticated patient can create an appointment for an available schedule.
        """
        # We need a fresh available schedule for this test
        new_available_schedule = Schedule.objects.create(doctor=self.doctor, date='2025-12-27', start_time='10:00', end_time='10:30', is_available=True)
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('appointment-list')
        data = {'schedule': new_available_schedule.pk}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Appointment.objects.filter(patient=self.patient1, schedule=new_available_schedule).exists())

        # Verify the schedule is now unavailable
        new_available_schedule.refresh_from_db()
        self.assertFalse(new_available_schedule.is_available)

    def test_patient_cannot_create_appointment_for_unavailable_schedule(self):
        """
        Ensure a patient cannot create an appointment for a schedule that is not available.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('appointment-list')
        data = {'schedule': self.unavailable_schedule.pk}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patient_can_list_their_own_appointments(self):
        """
        Ensure a patient can retrieve a list of their own appointments.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('appointment-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.appointment1.id)

    def test_patient_cannot_list_other_patients_appointments(self):
        """
        Ensure a patient cannot see appointments belonging to another patient.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('appointment-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0) # Patient 2 should have no appointments

    def test_patient_can_cancel_their_own_appointment(self):
        """
        Ensure a patient can cancel an appointment they own.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)
        url = reverse('appointment-cancel', kwargs={'pk': self.appointment1.pk})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.appointment1.refresh_from_db()
        self.assertEqual(self.appointment1.status, 'cancelled')

        # Check if the schedule is available again
        self.available_schedule.refresh_from_db()
        self.assertTrue(self.available_schedule.is_available)

    def test_patient_cannot_cancel_another_patients_appointment(self):
        """
        Ensure a patient cannot cancel an appointment belonging to someone else.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        url = reverse('appointment-cancel', kwargs={'pk': self.appointment1.pk})
        response = self.client.patch(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # The original appointment should remain unchanged
        self.appointment1.refresh_from_db()
        self.assertEqual(self.appointment1.status, 'booked')
