import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import Login from '../Login.vue';
import apiService from '@/services/apiService';

// Mock the apiService
vi.mock('@/services/apiService', () => ({
  default: {
    login: vi.fn(),
  },
}));

describe('Login.vue', () => {
  it('renders a login form with email, password, and a button', () => {
    const wrapper = mount(Login);

    // Check for the title
    expect(wrapper.find('h2').text()).toBe('Login');

    // Check for form elements
    expect(wrapper.find('label[for="login-email"]').exists()).toBe(true);
    expect(wrapper.find('input#login-email').exists()).toBe(true);
    expect(wrapper.find('label[for="login-password"]').exists()).toBe(true);
    expect(wrapper.find('input#login-password').exists()).toBe(true);
    expect(wrapper.find('button[type="submit"]').exists()).toBe(true);
  });

  it('calls apiService.login with credentials on form submission', async () => {
    // Mock the login function to resolve successfully
    apiService.login.mockResolvedValue({ data: { token: 'fake-token' } });

    const wrapper = mount(Login);

    // Find form elements
    const emailInput = wrapper.find('input#login-email');
    const passwordInput = wrapper.find('input#login-password');
    const form = wrapper.find('form');

    // Set input values
    await emailInput.setValue('test@example.com');
    await passwordInput.setValue('password123');

    // Trigger form submission
    await form.trigger('submit.prevent');

    // Assert that apiService.login was called
    expect(apiService.login).toHaveBeenCalledTimes(1);
    expect(apiService.login).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'password123',
    });
  });

  it('emits "loggedIn" event on successful login', async () => {
    // Mock the login function
    apiService.login.mockResolvedValue({ data: { token: 'fake-token' } });
    const wrapper = mount(Login);

    await wrapper.find('input#login-email').setValue('test@example.com');
    await wrapper.find('input#login-password').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    // Check if the 'loggedIn' event was emitted
    expect(wrapper.emitted().loggedIn).toBeTruthy();
    expect(wrapper.emitted().loggedIn.length).toBe(1);
  });

  it('displays an error message on failed login', async () => {
    // Mock the login function to reject with an error
    const errorMessage = 'Login failed. Please check your credentials.';
    apiService.login.mockRejectedValue(new Error('Login failed'));

    const wrapper = mount(Login);

    await wrapper.find('input#login-email').setValue('test@example.com');
    await wrapper.find('input#login-password').setValue('password123');
    await wrapper.find('form').trigger('submit.prevent');

    // Wait for the DOM to update
    await wrapper.vm.$nextTick();

    // Assert that the error message is displayed
    expect(wrapper.find('p').text()).toBe(errorMessage);
  });
});
