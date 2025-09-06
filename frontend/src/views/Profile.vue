<template>
  <div class="profile-container">
    <h1>個人資訊</h1>
    <div v-if="user" class="user-info">
      <p><strong>姓名:</strong> {{ user.name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>生日:</strong> {{ user.birthday }}</p>
      <p><strong>手機:</strong> {{ user.phone }}</p>
    </div>
    <div v-else>
      <p>正在載入使用者資訊...</p>
    </div>

    <h2 class="appointments-title">歷史預約紀錄</h2>
    <div v-if="appointments.length > 0" class="appointments-list">
      <div v-for="appointment in appointments" :key="appointment.id" class="appointment-card">
        <p><strong>醫師:</strong> {{ appointment.doctor_name }}</p>
        <p><strong>科別:</strong> {{ appointment.doctor_specialty }}</p>
        <p><strong>日期:</strong> {{ formatDate(appointment.schedule_date) }}</p>
        <p><strong>時間:</strong> {{ formatTime(appointment.schedule_start_time) }}</p>
        <p><strong>狀態:</strong> <span :class="`status-${appointment.status}`">{{ translateStatus(appointment.status) }}</span></p>
      </div>
    </div>
    <div v-else>
      <p>沒有歷史預約紀錄。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiService from '@/services/apiService';

const user = ref(null);
const appointments = ref([]);

onMounted(async () => {
  try {
    const userResponse = await apiService.getProfile();
    user.value = userResponse.data;

    const appointmentsResponse = await apiService.getAppointments();
    appointments.value = appointmentsResponse.data;
  } catch (error) {
    console.error('無法獲取個人資訊或預約紀錄:', error);
    // 根據錯誤情況，可以考慮導向登入頁面
  }
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const formatTime = (timeString) => {
  // 假設時間格式是 HH:MM:SS，我們只需要 HH:MM
  return timeString.substring(0, 5);
};

const translateStatus = (status) => {
  const statusMap = {
    booked: '已預約',
    cancelled: '已取消',
    completed: '已完成',
  };
  return statusMap[status] || status;
};
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

h1, .appointments-title {
  border-bottom: 2px solid #42b983;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.user-info {
  margin-bottom: 2rem;
}

.user-info p {
  margin: 0.5rem 0;
  font-size: 1.1rem;
}

.appointments-list {
  display: grid;
  gap: 1.5rem;
}

.appointment-card {
  padding: 1.5rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  transition: box-shadow 0.3s ease;
}

.appointment-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.appointment-card p {
  margin: 0.4rem 0;
}

.status-booked {
  color: #28a745;
  font-weight: bold;
}

.status-cancelled {
  color: #dc3545;
  font-weight: bold;
}

.status-completed {
  color: #6c757d;
  font-weight: bold;
}
</style>
