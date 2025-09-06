<template>
  <div class="confirmation-container">
    <div class="card text-center">
      <div class="card-header">
        <h2>預約成功</h2>
      </div>
      <div class="card-body">
        <p class="card-text">您的預約已確認。</p>
        <div v-if="appointment" class="appointment-details">
          <p><strong>醫師:</strong> {{ appointment.doctor_name }}</p>
          <p><strong>科別:</strong> {{ appointment.doctor_specialty }}</p>
          <p><strong>日期:</strong> {{ formatDate(appointment.schedule_date) }}</p>
          <p><strong>時間:</strong> {{ formatTime(appointment.schedule_start_time) }}</p>
        </div>
        <router-link to="/me" class="btn btn-primary">查看我的預約</router-link>
        <router-link to="/" class="btn btn-secondary">返回首頁</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const appointment = ref(null);

onMounted(() => {
  if (window.history.state.appointment) {
    appointment.value = window.history.state.appointment;
  }
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString();
};

const formatTime = (timeString) => {
  return timeString.substring(0, 5);
};
</script>

<style scoped>
.confirmation-container {
  max-width: 600px;
  margin: 3rem auto;
}

.card-header h2 {
  color: #28a745;
  font-weight: bold;
}

.appointment-details {
  margin: 2rem 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 5px;
}

.btn {
  margin: 0 0.5rem;
}
</style>
