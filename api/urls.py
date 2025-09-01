from django.urls import path
from .views import PatientRegistrationView, CustomAuthToken

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
]
