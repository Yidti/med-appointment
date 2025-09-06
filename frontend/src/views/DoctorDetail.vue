<template>
  <main class="doctor-detail-page">
    <div class="container py-5">
      <div v-if="doctor">
        <!-- Doctor Profile Section -->
        <div class="row mb-5">
          <div class="col-md-4 text-center">
            <img :src="`https://i.pravatar.cc/150?img=${doctor.id}`" class="img-fluid rounded-circle mb-3" alt="Doctor" style="width: 150px; height: 150px;">
            <h2 class="h4">{{ doctor.name }}</h2>
            <h3 class="h5 text-primary fw-bold">{{ doctor.specialty }}</h3>
            <p class="text-muted">{{ doctor.department }}</p>
          </div>
          <div class="col-md-8">
            <div class="card shadow-sm border-0">
              <div class="card-body p-4">
                <h4 class="card-title mb-4">Book an Appointment</h4>
                
                <!-- Schedule/Time Slots -->
                <div v-if="loadingSchedule" class="text-center">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>

                <div v-else-if="Object.keys(groupedSchedules).length > 0">
                  <div v-for="(slots, date) in groupedSchedules" :key="date" class="mb-4">
                    <h5 class="mb-3">{{ formatDate(date) }}</h5>
                    <div class="list-group">
                      <button 
                        v-for="slot in slots" 
                        :key="slot.id" 
                        type="button" 
                        class="list-group-item list-group-item-action text-center"
                        @click="selectSlot(slot)"
                        :class="{ 'active': selectedSlot && selectedSlot.id === slot.id }"
                      >
                        {{ slot.time }}
                      </button>
                    </div>
                  </div>
                </div>

                <div v-else>
                  <p class="text-muted">No available appointments for this doctor.</p>
                </div>

                <!-- Booking Button -->
                <div class="d-grid mt-4" v-if="selectedSlot">
                  <button class="btn btn-primary btn-lg" @click="confirmBooking">Book Appointment for {{ selectedSlot.time }}</button>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else class="text-center">
        <p class="lead">Loading doctor details...</p>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiService from '@/services/apiService';

const route = useRoute();
const router = useRouter();
const doctor = ref(null);
const errorMessage = ref('');
const allSchedules = ref([]);
const selectedSlot = ref(null);
const loadingSchedule = ref(false);

const groupedSchedules = computed(() => {
  return allSchedules.value.reduce((acc, slot) => {
    const date = slot.date;
    if (!acc[date]) {
      acc[date] = [];
    }
    acc[date].push({
      id: slot.id,
      time: new Date(`1970-01-01T${slot.start_time}`).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true })
    });
    return acc;
  }, {});
});

const formatDate = (dateString) => {
  const date = new Date(dateString);
  // Adjust for timezone offset to prevent date from changing
  const userTimezoneOffset = date.getTimezoneOffset() * 60000;
  const adjustedDate = new Date(date.getTime() + userTimezoneOffset);
  return adjustedDate.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
};

const fetchSchedule = async () => {
  if (!doctor.value) return;
  loadingSchedule.value = true;
  selectedSlot.value = null;
  allSchedules.value = [];
  try {
    const response = await apiService.getSchedules(doctor.value.id);
    allSchedules.value = response.data;
  } catch (error) {
    console.error('Failed to fetch schedule:', error);
    errorMessage.value = 'Could not load schedule.';
  } finally {
    loadingSchedule.value = false;
  }
};

const selectSlot = (slot) => {
  selectedSlot.value = slot;
};

const confirmBooking = async () => {
  if (!selectedSlot.value) return;
  try {
    await apiService.createAppointment(selectedSlot.value.id);

    const bookedSchedule = allSchedules.value.find(s => s.id === selectedSlot.value.id);

    const appointmentDetails = {
      doctor_name: doctor.value.name,
      doctor_specialty: doctor.value.specialty,
      schedule_date: bookedSchedule.date,
      schedule_start_time: bookedSchedule.start_time,
    };

    router.push({
      name: 'Confirmation',
      state: { appointment: appointmentDetails },
    });
  } catch (error) {
    console.error('Booking failed:', error);
    alert('Failed to book appointment. The slot may have just been taken. Please try another.');
    fetchSchedule();
  }
};

onMounted(async () => {
  const doctorId = route.params.id;
  try {
    const response = await apiService.getDoctor(doctorId);
    doctor.value = response.data;
    await fetchSchedule();
  } catch (error) {
    console.error('Failed to fetch doctor details:', error);
    errorMessage.value = 'Could not load doctor details. Please try again later.';
  }
});
</script>

<style scoped>
.doctor-detail-page {
  background-color: #f8f9fa;
}
.list-group-item-action.active {
  z-index: 2;
  color: #fff;
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>