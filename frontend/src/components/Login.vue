<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="login-email">Email:</label>
        <input type="email" id="login-email" v-model="email" required>
      </div>
      <div>
        <label for="login-password">Password:</label>
        <input type="password" id="login-password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import apiService from '@/services/apiService';

const email = ref('');
const password = ref('');
const errorMessage = ref('');

const emit = defineEmits(['loggedIn']);

const handleLogin = async () => {
  try {
    const credentials = {
      email: email.value,
      password: password.value,
    };
    const response = await apiService.login(credentials);
    localStorage.setItem('token', response.data.token);
    emit('loggedIn');
  } catch (error) {
    errorMessage.value = 'Login failed. Please check your credentials.';
    console.error(error);
  }
};
</script>
