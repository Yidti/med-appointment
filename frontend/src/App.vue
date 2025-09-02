<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <router-link class="navbar-brand" to="/">Medical Appointment</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" active-class="active" to="/">Home</router-link>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn">
              <router-link class="nav-link" active-class="active" to="/doctors">Doctors</router-link>
            </li>
          </ul>
          <ul class="navbar-nav">
            <li class="nav-item" v-if="!auth.isLoggedIn">
              <router-link class="btn btn-outline-light me-2" to="/login">Login</router-link>
            </li>
            <li class="nav-item" v-if="!auth.isLoggedIn">
              <router-link class="btn btn-light" to="/register">Register</router-link>
            </li>
            <li class="nav-item" v-if="auth.isLoggedIn">
              <a class="btn btn-outline-light" href="#" @click.prevent="handleLogout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container-fluid my-5 px-lg-5">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from './stores/auth';

const auth = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  auth.logout();
  router.push('/login');
};
</script>

<style>
body {
  background-color: #f8f9fa;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.navbar-brand {
  font-weight: 600;
}

/* Add some transition effects */
.btn {
  transition: all 0.3s ease-in-out;
}
</style>
