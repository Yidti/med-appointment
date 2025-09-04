import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import DoctorDetail from '../DoctorDetail.vue';
import apiService from '@/services/apiService';

// 1. Mock the entire apiService module
vi.mock('@/services/apiService', () => ({
  default: {
    getDoctor: vi.fn(),
    getSchedules: vi.fn(),
    createAppointment: vi.fn(),
  },
}));

// 2. Mock the vue-router dependency
const mockDoctorId = '1';
vi.mock('vue-router', () => ({
  useRoute: () => ({
    params: {
      id: mockDoctorId,
    },
  }),
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

describe('DoctorDetail.vue', () => {
  // Reset mocks before each test to ensure isolation
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock window.alert to prevent jsdom errors
    vi.spyOn(window, 'alert').mockImplementation(() => {});
  });

  it('should fetch and display doctor details on mount', async () => {
    const mockDoctor = { id: 1, name: 'Dr. API Fetched', specialty: 'TDD' };
    apiService.getDoctor.mockResolvedValue({ data: mockDoctor });
    // Mock schedule call during mount to prevent error
    apiService.getSchedules.mockResolvedValue({ data: [] });

    const wrapper = mount(DoctorDetail);

    await new Promise(resolve => setTimeout(resolve, 0));

    expect(apiService.getDoctor).toHaveBeenCalledWith(mockDoctorId);
    expect(wrapper.text()).toContain(mockDoctor.name);
    expect(wrapper.text()).toContain(mockDoctor.specialty);
  });

  it('fetches schedules when the date is changed', async () => {
    const mockDoctor = { id: 1, name: 'Dr. API Fetched', specialty: 'TDD' };
    apiService.getDoctor.mockResolvedValue({ data: mockDoctor });
    apiService.getSchedules.mockResolvedValue({ data: [] }); // Initial call

    const wrapper = mount(DoctorDetail);
    await new Promise(resolve => setTimeout(resolve, 0)); // Wait for mount

    // Find the date input and change its value
    const newDate = '2025-11-22';
    const dateInput = wrapper.find('input[type="date"]');
    await dateInput.setValue(newDate);

    // The @change event should trigger fetchSchedule
    expect(apiService.getSchedules).toHaveBeenCalledWith(mockDoctor.id, newDate);
  });

  it('calls createAppointment when a slot is selected and button is clicked', async () => {
    const mockDoctor = { id: 1, name: 'Dr. API Fetched', specialty: 'TDD' };
    const mockSchedule = [{ id: 99, start_time: '10:00:00', is_available: true }];
    apiService.getDoctor.mockResolvedValue({ data: mockDoctor });
    apiService.getSchedules.mockResolvedValue({ data: mockSchedule });
    apiService.createAppointment.mockResolvedValue({ data: {} }); // Mock successful booking

    const wrapper = mount(DoctorDetail);
    await new Promise(resolve => setTimeout(resolve, 0)); // Wait for mount and schedule fetch
    await wrapper.vm.$nextTick(); // Wait for DOM update

    // Find and click the available slot
    const slotButton = wrapper.find('.list-group-item-action');
    await slotButton.trigger('click');
    await wrapper.vm.$nextTick();

    // Find and click the booking button
    const bookingButton = wrapper.find('.btn-primary');
    await bookingButton.trigger('click');

    expect(apiService.createAppointment).toHaveBeenCalledWith(mockSchedule[0].id);
  });
});
