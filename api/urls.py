from django.urls import path
from .views import PatientRegistrationView, CustomAuthToken, UserProfileView, DoctorListView, DoctorDetailView

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
]
