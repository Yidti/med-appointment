import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount, flushPromises } from '@vue/test-utils';
import { createRouter, createWebHistory } from 'vue-router';
import Register from '../Register.vue';
import apiService from '@/services/apiService';

// Mock the entire apiService module
vi.mock('@/services/apiService', () => ({
  default: {
    register: vi.fn(),
  },
}));

// Create a router instance for the tests
const router = createRouter({
  history: createWebHistory(),
  routes: [], // No routes needed for this component's test
});

// Helper function to fill and submit the form
const fillAndSubmitForm = async (wrapper, userData) => {
  await wrapper.find('#name').setValue(userData.name);
  await wrapper.find('#email').setValue(userData.email);
  await wrapper.find('#password').setValue(userData.password);
  if (userData.phone) await wrapper.find('#phone').setValue(userData.phone);
  if (userData.birthday) await wrapper.find('#birthday').setValue(userData.birthday);
  await wrapper.find('form').trigger('submit.prevent');
};

describe('Register.vue', () => {
  let wrapper;
  const userData = {
    name: 'Test User',
    email: 'test@example.com',
    password: 'password123',
    phone: '1234567890',
    birthday: '2000-01-01',
  };

  // Reset mocks and mount component before each test
  beforeEach(() => {
    vi.clearAllMocks();
    wrapper = mount(Register, {
      global: {
        plugins: [router],
      },
    });
  });

  it('renders a register form', () => {
    expect(wrapper.find('h3').text()).toBe('Create Account');
    expect(wrapper.find('form').exists()).toBe(true);
  });

  it('calls apiService.register with form data on submit', async () => {
    await fillAndSubmitForm(wrapper, userData);
    expect(apiService.register).toHaveBeenCalledWith(userData);
  });

  it('displays a success message on successful registration', async () => {
    // Arrange: Mock the API to resolve successfully
    vi.mocked(apiService.register).mockResolvedValue({});

    // Act: Fill and submit the form
    await fillAndSubmitForm(wrapper, {
      name: 'Test User',
      email: 'test@example.com',
      password: 'password123',
    });

    // Wait for promises to resolve and DOM to update
    await flushPromises();

    // Assert: Check for the success message
    const successAlert = wrapper.find('.alert-success');
    expect(successAlert.exists()).toBe(true);
    expect(successAlert.text()).toContain('Registration successful!');
  });
});
