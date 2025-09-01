from rest_framework import serializers
from .models import Patient
from django.contrib.auth import authenticate

class PatientSerializer(serializers.ModelSerializer):
    # We are making password write_only so it's not returned in the response.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Patient
        # Note: AbstractUser has first_name, last_name. We are using 'username' as a proxy for name for now.
        fields = ('id', 'username', 'email', 'password', 'phone', 'birthday')

    def create(self, validated_data):
        """
        Use Django's `create_user` method to handle password hashing.
        """
        user = Patient.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
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
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Since we set USERNAME_FIELD = 'email' in our Patient model,
            # Django's authenticate function will correctly handle email as the username.
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs