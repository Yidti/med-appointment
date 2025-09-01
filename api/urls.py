from django.urls import path
from .views import (
    PatientRegistrationView, CustomAuthToken, UserProfileView, 
    DoctorListView, DoctorDetailView, ScheduleListView,
    AppointmentListCreateView, AppointmentCancelView
)

urlpatterns = [
    path('register/', PatientRegistrationView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('schedules/', ScheduleListView.as_view(), name='schedule-list'),
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
]
