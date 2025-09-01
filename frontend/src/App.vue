<template>
  <div id="app">
    <div v-if="!isLoggedIn" class="container">
      <div class="column">
        <Register @registered="handleRegistration" />
      </div>
      <div class="column">
        <Login @loggedIn="handleLogin" />
      </div>
    </div>
    <div v-else>
      <button @click="handleLogout">Logout</button>
      <DoctorList />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Register from './components/Register.vue';
import Login from './components/Login.vue';
import DoctorList from './components/DoctorList.vue';

const isLoggedIn = ref(!!localStorage.getItem('token'));

const handleRegistration = () => {
  // For now, just show an alert. In a real app, you might want to automatically log the user in.
  alert('Registration successful! Please log in.');
};

const handleLogin = () => {
  isLoggedIn.value = true;
};

const handleLogout = () => {
  localStorage.removeItem('token');
  isLoggedIn.value = false;
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.container {
  display: flex;
  justify-content: space-around;
}

.column {
  width: 45%;
}
</style>