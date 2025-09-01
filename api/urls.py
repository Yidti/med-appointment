from django.urls import path
from .views import PatientRegistrationView, CustomAuthToken, UserProfileView

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
