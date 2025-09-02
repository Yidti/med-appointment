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
                
                <!-- Date Picker -->
                <div class="mb-4">
                  <label for="appointment-date" class="form-label">Select a Date:</label>
                  <input type="date" class="form-control" id="appointment-date" v-model="selectedDate" @change="fetchSchedule">
                </div>

                <!-- Schedule/Time Slots -->
                <h5>Available Slots for {{ formattedDate }}</h5>
                <div v-if="loadingSchedule" class="text-center">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                  </div>
                </div>
                <div v-else-if="availableSlots.length > 0" class="list-group">
                  <button 
                    v-for="slot in availableSlots" 
                    :key="slot.id" 
                    type="button" 
                    class="list-group-item list-group-item-action text-center"
                    @click="selectSlot(slot)"
                    :class="{ 'active': selectedSlot && selectedSlot.id === slot.id }"
                  >
                    {{ slot.time }}
                  </button>
                </div>
                <div v-else>
                  <p class="text-muted">No available slots for this date. Please select another date.</p>
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

// Mock data - in a real app, this would be in a store or fetched
const mockDoctors = [
  { id: 1, name: 'Dr. Alice Williams', specialty: 'Cardiology', department: 'Heart & Vascular Institute' },
  { id: 2, name: 'Dr. John Smith', specialty: 'Neurology', department: 'Brain & Spine Center' },
  { id: 3, name: 'Dr. Patricia Jones', specialty: 'Dermatology', department: 'Skin Care Clinic' },
  { id: 4, name: 'Dr. Michael Brown', specialty: 'Orthopedics', department: 'Bone & Joint Health' },
  { id: 5, name: 'Dr. Linda Davis', specialty: 'Pediatrics', department: 'Children\'s Health' },
  { id: 6, name: 'Dr. Robert Miller', specialty: 'Oncology', department: 'Cancer Treatment Center' },
];

// Mock schedule data
const mockSchedules = {
  '1': [{id: 101, time: '09:00 AM'}, {id: 102, time: '11:00 AM'}, {id: 103, time: '02:00 PM'}],
  '3': [{id: 301, time: '10:00 AM'}, {id: 302, time: '03:00 PM'}],
  '5': [{id: 501, time: '09:30 AM'}, {id: 502, time: '10:30 AM'}, {id: 503, time: '11:30 AM'}],
};

const route = useRoute();
const router = useRouter();
const doctor = ref(null);
const selectedDate = ref(new Date().toISOString().slice(0, 10));
const availableSlots = ref([]);
const selectedSlot = ref(null);
const loadingSchedule = ref(false);

const formattedDate = computed(() => {
  if (!selectedDate.value) return '';
  const date = new Date(selectedDate.value);
  return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
});

const fetchSchedule = () => {
  loadingSchedule.value = true;
  selectedSlot.value = null;
  // Simulate API call
  setTimeout(() => {
    const doctorId = route.params.id;
    // This is a very basic mock logic. A real app would have more complex date-based logic.
    availableSlots.value = mockSchedules[doctorId] || [];
    loadingSchedule.value = false;
  }, 500);
};

const selectSlot = (slot) => {
  selectedSlot.value = slot;
};

const confirmBooking = () => {
  if (!selectedSlot.value) return;
  // In a real app, you would call an API to create the appointment.
  // Then navigate to a confirmation page.
  alert(`Appointment booked with ${doctor.value.name} at ${selectedSlot.value.time} on ${formattedDate.value}!`);
  router.push('/appointments'); // Assuming an appointments history page exists
};

onMounted(() => {
  const doctorId = parseInt(route.params.id);
  doctor.value = mockDoctors.find(d => d.id === doctorId);
  fetchSchedule();
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
