<template>
  <div class="container col-xxl-8 px-4 py-5">
    <div class="row flex-lg-row-reverse align-items-center g-5 py-5">
      <div class="col-10 col-sm-8 col-lg-6">
        <img src="https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=2940&auto=format&fit=crop" class="d-block mx-lg-auto img-fluid rounded shadow" alt="Doctor with tablet" width="700" height="500" loading="lazy">
      </div>
      <div class="col-lg-6">
        <h1 class="display-5 fw-bold lh-1 mb-3">Medical Appointment System</h1>
        <p class="lead">Your health, simplified. Easily book and manage your medical appointments online with our intuitive platform. Find doctors, check schedules, and book your slot in just a few clicks.</p>
        <div class="d-grid gap-2 d-md-flex justify-content-md-start" v-if="!auth.isLoggedIn">
          <router-link to="/login" class="btn btn-primary btn-lg px-4 me-md-2">Login</router-link>
          <router-link to="/register" class="btn btn-outline-secondary btn-lg px-4">Register</router-link>
        </div>
         <div class="d-grid gap-2 d-md-flex justify-content-md-start" v-else>
          <router-link to="/doctors" class="btn btn-primary btn-lg px-4 me-md-2">Find a Doctor</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '../stores/auth';

const auth = useAuthStore();
</script>

<style scoped>
.lead {
  color: #6c757d;
}
</style>
