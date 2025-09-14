from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from .serializers import PatientSerializer, EmailAuthTokenSerializer, DoctorSerializer, ScheduleSerializer, AppointmentSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import Patient, Doctor, Schedule, Appointment
from django.utils import timezone

class PatientRegistrationView(APIView):
    """
    Allows new patients to register.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class UserProfileView(APIView):
    """
    Handles retrieving and updating authenticated user's profile.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Return the authenticated user's profile information.
        """
        serializer = PatientSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, format=None):
        """
        Update the authenticated user's profile.
        """
        user = request.user
        # We pass partial=True to allow partial updates
        serializer = PatientSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorListView(generics.ListAPIView):
    """
    Provides a list of all doctors.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]


class DoctorDetailView(generics.RetrieveAPIView):
    """
    Provides details of a single doctor.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]


from django.utils import timezone

class ScheduleListView(generics.ListAPIView):
    """
    List schedules, filtered by doctor_id and date.
    If no date is provided, returns all future available schedules for the doctor.
    """
    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Optionally restricts the returned schedules to a given doctor and date,
        by filtering against `doctor_id` and `date` query parameters in the URL.
        """
        queryset = Schedule.objects.all()
        doctor_id = self.request.query_params.get('doctor_id')
        date = self.request.query_params.get('date')

        if doctor_id is not None:
            queryset = queryset.filter(doctor__pk=doctor_id)
        
        if date is not None:
            queryset = queryset.filter(date=date)
        else:
            # If no date is specified, return all available schedules from today onwards
            queryset = queryset.filter(date__gte=timezone.now().date(), is_available=True)
            
        return queryset

class AppointmentListCreateView(generics.ListCreateAPIView):
    """
    List all appointments for the logged-in user, or create a new appointment.
    """
    authentication_classes = [TokenAuthentication]
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the appointments
        for the currently authenticated user.
        """
        return Appointment.objects.filter(patient=self.request.user)

    def perform_create(self, serializer):
        schedule = serializer.validated_data['schedule']
        
        if not schedule.is_available:
            raise serializers.ValidationError({"error": "This schedule is not available."})

        # Set the patient to the logged-in user
        appointment = serializer.save(patient=self.request.user)
        
        # Mark the schedule as unavailable
        schedule.is_available = False
        schedule.save()

class AppointmentCancelView(APIView):
    """
    Allows a patient to cancel their appointment.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, format=None):
        try:
            appointment = Appointment.objects.get(pk=pk, patient=request.user)
        except Appointment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Check if the appointment is already cancelled or completed
        if appointment.status != 'booked':
            return Response({'error': 'This appointment cannot be cancelled.'}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = 'cancelled'
        appointment.save()

        # Make the schedule available again
        schedule = appointment.schedule
        schedule.is_available = True
        schedule.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
