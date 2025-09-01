<template>
  <div>
    <h2>Register</h2>
    <form @submit.prevent="handleRegister">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="name" required>
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <div>
        <label for="phone">Phone:</label>
        <input type="text" id="phone" v-model="phone">
      </div>
      <div>
        <label for="birthday">Birthday:</label>
        <input type="date" id="birthday" v-model="birthday">
      </div>
      <button type="submit">Register</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import apiService from '@/services/apiService';

const name = ref('');
const email = ref('');
const password = ref('');
const phone = ref('');
const birthday = ref('');
const errorMessage = ref('');

const emit = defineEmits(['registered']);

const handleRegister = async () => {
  try {
    const userData = {
      name: name.value,
      email: email.value,
      password: password.value,
      phone: phone.value,
      birthday: birthday.value,
    };
    await apiService.register(userData);
    emit('registered');
  } catch (error) {
    errorMessage.value = 'Registration failed. Please check your input.';
    console.error(error);
  }
};
</script>
