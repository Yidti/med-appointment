from rest_framework import serializers
from .models import Patient, Doctor, Schedule, Appointment
from django.contrib.auth import authenticate

class PatientSerializer(serializers.ModelSerializer):
    # The frontend sends 'name', and we make it write-only.
    first_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        # 'username' is handled internally, not exposed to the client for registration.
        fields = ('id', 'username', 'first_name', 'email', 'password', 'phone', 'birthday')
        read_only_fields = ('id', 'username',)

    def create(self, validated_data):
        """
        Use Django's `create_user` method to handle password hashing.
        We use the email as the username, as specified in the Patient model's USERNAME_FIELD.
        The 'name' from the frontend is used for 'first_name'.
        """
        user = Patient.objects.create_user(
            username=validated_data['email'],  # Use email for the username field
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),  # Use first_name
            phone=validated_data.get('phone'),
            birthday=validated_data.get('birthday')
        )
        return user

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            password = attrs.get('password')

            print(f"[Auth Debug] Email: {email}, Password: {password}")
            if email and password:
                # Since we set USERNAME_FIELD = 'email' in our Patient model,
                # Django's authenticate function will correctly handle email as the username.
                user = authenticate(request=self.context.get('request'),
                                    username=email, password=password)
                print(f"[Auth Debug] User object: {user}")

                if not user:
                    msg = 'Unable to log in with provided credentials.'
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = 'Must include "email" and "password".'
                raise serializers.ValidationError(msg, code='authorization')

            attrs['user'] = user
            return attrs
        except Exception as e:
            raise serializers.ValidationError(str(e))


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'specialty', 'department')


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'doctor', 'date', 'start_time', 'end_time', 'is_available')


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'patient', 'schedule', 'status', 'created_at')
        read_only_fields = ('patient', 'status', 'created_at')

    def validate_schedule(self, value):
        """
        Check if the schedule is available.
        """
        if not value.is_available:
            raise serializers.ValidationError("This schedule is not available.")
        return value

