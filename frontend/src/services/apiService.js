import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in the headers
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  // Patient/User
  register(userData) {
    return apiClient.post('/register/', userData);
  },
  login(credentials) {
    return apiClient.post('/login/', credentials);
  },
  getProfile() {
    return apiClient.get('/me/');
  },
  updateProfile(profileData) {
    return apiClient.put('/me/', profileData);
  },

  // Doctors
  getDoctors() {
    return apiClient.get('/doctors/');
  },
  getDoctor(id) {
    return apiClient.get(`/doctors/${id}/`);
  },

  // Schedules
  getSchedules(doctorId, date) {
    let url = `/schedules/?doctor_id=${doctorId}`;
    if (date) {
      url += `&date=${date}`;
    }
    return apiClient.get(url);
  },

  // Appointments
  createAppointment(scheduleId) {
    return apiClient.post('/appointments/', { schedule: scheduleId });
  },
  getAppointments() {
    return apiClient.get('/appointments/');
  },
  cancelAppointment(id) {
    return apiClient.patch(`/appointments/${id}/cancel/`);
  },
};
