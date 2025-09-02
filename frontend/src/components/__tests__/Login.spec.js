import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import { createPinia } from 'pinia';
import { createRouter, createWebHistory } from 'vue-router';
import Login from '../Login.vue';
import apiService from '@/services/apiService';

// Mock the entire apiService module
vi.mock('@/services/apiService', () => ({
  default: {
    login: vi.fn(),
  },
}));

// Create a router instance for the tests
const router = createRouter({
  history: createWebHistory(),
  // Add a catch-all route to silence 'No match found' warnings
  routes: [{ path: '/:pathMatch(.*)*', component: {} }],
});

describe('Login.vue', () => {
  let pinia;

  // Use beforeEach to ensure a fresh Pinia store and cleared mocks for each test
  beforeEach(() => {
    pinia = createPinia();
    vi.clearAllMocks();
  });

  // Helper function to mount the component with necessary plugins
  const createWrapper = () => {
    return mount(Login, {
      global: {
        plugins: [pinia, router],
      },
    });
  };

  it('renders the login form correctly', () => {
    const wrapper = createWrapper();
    expect(wrapper.find('h3').text()).toBe('Login');
    expect(wrapper.find('input#login-email').exists()).toBe(true);
    expect(wrapper.find('input#login-password').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it('calls apiService.login and redirects on successful submission', async () => {
    // Arrange: Mock the successful API response
    apiService.login.mockResolvedValue({ data: { token: 'fake-token' } });
    const pushSpy = vi.spyOn(router, 'push');
    const wrapper = createWrapper();

    // Act: Simulate user input and form submission
    await wrapper.find('input#login-email').setValue('test@example.com');
    await wrapper.find('input#login-password').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    // Assert: Check that the API was called and router was used for redirection
    expect(apiService.login).toHaveBeenCalledTimes(1);
    expect(apiService.login).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
    expect(pushSpy).toHaveBeenCalledWith('/doctors');

    pushSpy.mockRestore();
  });

  it('displays an error message on failed login', async () => {
    // Arrange: Mock the failed API response
    apiService.login.mockRejectedValue(new Error('Login failed'));
    const wrapper = createWrapper();

    // Act: Simulate user input and form submission
    await wrapper.find('input#login-email').setValue('test@example.com');
    await wrapper.find('input#login-password').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    // Assert: Wait for the DOM to update and check for the error message
    await wrapper.vm.$nextTick();
    expect(wrapper.find('.alert-danger').text()).toBe('Login failed. Please check your credentials.');
  });
});
