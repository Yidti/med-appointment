<template>
  <div>
    <h2>Doctors</h2>
    <ul v-if="doctors.length">
      <li v-for="doctor in doctors" :key="doctor.id">
        {{ doctor.name }} - {{ doctor.specialty }}
      </li>
    </ul>
    <p v-else>No doctors available.</p>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiService from '@/services/apiService';

const doctors = ref([]);
const errorMessage = ref('');

onMounted(async () => {
  try {
    const response = await apiService.getDoctors();
    doctors.value = response.data;
  } catch (error) {
    errorMessage.value = 'Failed to load doctors.';
    console.error(error);
  }
});
</script>
