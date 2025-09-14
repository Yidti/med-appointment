<template>
  <div class="login-page bg-light">
    <div class="container">
      <div class="row justify-content-center align-items-center min-vh-100">
        <div class="col-12 col-md-8 col-lg-6">
          <div class="card shadow-sm border-0 rounded-lg">
            <div class="card-body p-4 p-sm-5">
              <h3 class="text-center fw-bold mb-4">Login</h3>
              <form @submit.prevent="handleLogin">
                <div class="form-floating mb-3">
                  <input class="form-control" id="login-email" type="email" placeholder="name@example.com" v-model="email" required />
                  <label for="login-email">Email address</label>
                </div>
                <div class="form-floating mb-3">
                  <input class="form-control" id="login-password" type="password" placeholder="Password" v-model="password" required />
                  <label for="login-password">Password</label>
                </div>
                <div class="d-grid gap-2 mt-4">
                  <button type="submit" class="btn btn-primary btn-lg">Login</button>
                </div>
              </form>
              <div class="text-center mt-4">
                <router-link to="/register" class="small">Need an account? Sign up!</router-link>
              </div>
            </div>
          </div>
          <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
            {{ errorMessage }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import apiService from '@/services/apiService';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const auth = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  errorMessage.value = '';
  try {
    const credentials = {
      email: email.value,
      password: password.value,
    };
    const response = await apiService.login(credentials);
    auth.setToken(response.data.token);
    console.log('Login successful, attempting to redirect...');
    router.push('/doctors');
    console.log('Redirect call finished.');
  } catch (error) {
    errorMessage.value = 'Login failed. Please check your credentials.';
    console.error(error);
    auth.logout();
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
}
.card {
  background-color: #ffffff;
}
</style>
