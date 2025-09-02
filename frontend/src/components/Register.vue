<template>
  <div class="row justify-content-center">
    <div class="col-sm-12 col-md-10 col-lg-8 col-xl-7">
      <div class="card shadow-lg border-0 rounded-lg mt-5">
        <div class="card-header"><h3 class="text-center font-weight-light my-4">Create Account</h3></div>
        <div class="card-body">
          <form @submit.prevent="handleRegister">
            <div class="row mb-3">
              <div class="col-md-6">
                <div class="form-floating mb-3 mb-md-0">
                  <input class="form-control" id="name" type="text" placeholder="Enter your name" v-model="name" required />
                  <label for="name">Name</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating">
                  <input class="form-control" id="email" type="email" placeholder="name@example.com" v-model="email" required />
                  <label for="email">Email address</label>
                </div>
              </div>
            </div>
            <div class="form-floating mb-3">
              <input class="form-control" id="password" type="password" placeholder="Create a password" v-model="password" required />
              <label for="password">Password</label>
            </div>
            <div class="row mb-3">
              <div class="col-md-6">
                <div class="form-floating mb-3 mb-md-0">
                  <input class="form-control" id="phone" type="tel" placeholder="Enter your phone number" v-model="phone" />
                  <label for="phone">Phone Number</label>
                </div>
              </div>
              <div class="col-md-6">
                <div class="form-floating mb-3 mb-md-0">
                  <input class="form-control" id="birthday" type="date" placeholder="Enter your birthday" v-model="birthday" />
                  <label for="birthday">Birthday</label>
                </div>
              </div>
            </div>
            <div class="mt-4 mb-0">
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-block">Create Account</button>
              </div>
            </div>
          </form>
        </div>
        <div class="card-footer text-center py-3">
          <div class="small"><router-link to="/login">Have an account? Go to login</router-link></div>
        </div>
      </div>
      <div v-if="successMessage" class="alert alert-success mt-3" role="alert">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-3" role="alert">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiService from '@/services/apiService';

const name = ref('');
const email = ref('');
const password = ref('');
const phone = ref('');
const birthday = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const router = useRouter();

const handleRegister = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  try {
    const userData = {
      name: name.value,
      email: email.value,
      password: password.value,
      phone: phone.value,
      birthday: birthday.value,
    };
    // await apiService.register(userData);
    successMessage.value = 'Registration successful! Redirecting to login...';
    setTimeout(() => {
      router.push('/login');
    }, 2000);
  } catch (error) {
    errorMessage.value = 'Registration failed. Please check your input.';
    console.error(error);
  }
};
</script>

<style scoped>
.card-header, .card-footer {
  background-color: #f7f7f7;
}
</style>
