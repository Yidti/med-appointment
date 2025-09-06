<template>
  <main class="doctor-list-page">
    <div class="container py-5">
      <div class="text-center mb-5">
        <h2 class="mb-4">Find Your Doctor</h2>
        <p class="lead text-muted">Search for a specialist and book your appointment today.</p>
      </div>

      <!-- Search and Filter Bar -->
      <div class="row mb-5 justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="input-group input-group-lg">
            <input type="text" class="form-control" placeholder="Search by name or specialty..." v-model="searchQuery">
            <button class="btn btn-primary" type="button"><i class="bi bi-search"></i></button>
          </div>
        </div>
      </div>

      <!-- Doctor List -->
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div class="col" v-for="doctor in filteredDoctors" :key="doctor.id">
          <div class="card h-100 shadow-sm border-0 text-center">
            <div class="card-body p-4">
              <img :src="`https://i.pravatar.cc/150?img=${doctor.id}`" class="rounded-circle mb-3" alt="Doctor" width="100" height="100">
              <h5 class="card-title mb-1">{{ doctor.name }}</h5>
              <h6 class="card-subtitle mb-2 text-primary fw-bold">{{ doctor.specialty }}</h6>
              <p class="card-text text-muted small">{{ doctor.department }}</p>
              <router-link :to="`/doctors/${doctor.id}`" class="btn btn-outline-primary mt-3">View Schedule</router-link>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!filteredDoctors.length && !errorMessage" class="text-center mt-5">
          <p class="lead">No doctors found matching your criteria.</p>
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-5" role="alert">
          {{ errorMessage }}
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import apiService from '@/services/apiService';

const doctors = ref([]);
const searchQuery = ref('');
const errorMessage = ref('');

const filteredDoctors = computed(() => {
  if (!searchQuery.value) {
    return doctors.value;
  }
  const lowerCaseQuery = searchQuery.value.toLowerCase();
  return doctors.value.filter(doctor =>
    doctor.name.toLowerCase().includes(lowerCaseQuery) ||
    doctor.specialty.toLowerCase().includes(lowerCaseQuery)
  );
});

onMounted(async () => {
  try {
    const response = await apiService.getDoctors();
    doctors.value = response.data;
  } catch (error) {
    errorMessage.value = 'Failed to load doctors. Please make sure you are logged in and the server is running.';
    console.error('Error fetching doctors:', error);
  }
});
</script>

<style scoped>
.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.175) !important;
}
.rounded-circle {
  border: 3px solid #fff;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.text-primary {
    color: #0d6efd;
}
</style>
