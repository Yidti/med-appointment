import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import Profile from '../Profile.vue';
import apiService from '@/services/apiService';

// Mock the apiService
vi.mock('@/services/apiService', () => ({
  default: {
    getProfile: vi.fn(),
    getAppointments: vi.fn(),
  },
}));

describe('Profile.vue', () => {
  it('renders user information and appointments correctly', async () => {
    // Mock API responses
    const user = {
      name: 'Test User',
      email: 'test@example.com',
      birthday: '2000-01-01',
      phone: '1234567890',
    };
    const appointments = [
      {
        id: 1,
        doctor_name: 'Dr. Smith',
        doctor_specialty: 'Cardiology',
        schedule_date: '2025-10-10',
        schedule_start_time: '10:00:00',
        status: 'booked',
      },
    ];
    apiService.getProfile.mockResolvedValue({ data: user });
    apiService.getAppointments.mockResolvedValue({ data: appointments });

    // Mount the component
    const wrapper = mount(Profile);

    // Wait for the component to update
    await new Promise(resolve => setTimeout(resolve, 0));

    // Assert user information
    expect(wrapper.text()).toContain('Test User');
    expect(wrapper.text()).toContain('test@example.com');

    // Assert appointment information
    expect(wrapper.text()).toContain('Dr. Smith');
    expect(wrapper.text()).toContain('Cardiology');
    expect(wrapper.text()).toContain('已預約');
  });
});
