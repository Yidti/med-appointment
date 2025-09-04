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
    vi.spyOn(window, 'alert').mockImplementation(() => {});
  });

  it('fetches details and all schedules and displays them grouped by date', async () => {
    const mockDoctor = { id: '1', name: 'Dr. API Fetched', specialty: 'TDD' };
    const mockSchedules = [
      { id: 101, date: '2025-10-20', start_time: '09:00:00', is_available: true },
      { id: 102, date: '2025-10-21', start_time: '10:00:00', is_available: true },
      { id: 103, date: '2025-10-20', start_time: '11:00:00', is_available: true },
    ];
    apiService.getDoctor.mockResolvedValue({ data: mockDoctor });
    apiService.getSchedules.mockResolvedValue({ data: mockSchedules });

    const wrapper = mount(DoctorDetail);
    await new Promise(resolve => setTimeout(resolve, 0)); // Wait for promises
    await wrapper.vm.$nextTick(); // Wait for render

    // Assert new UI: date picker should NOT exist
    expect(wrapper.find('input[type="date"]').exists()).toBe(false);

    // Assert doctor details are shown
    expect(wrapper.text()).toContain(mockDoctor.name);

    // Assert schedules are fetched (without a date) and shown grouped by date
    expect(apiService.getSchedules).toHaveBeenCalledWith(mockDoctorId);
    expect(wrapper.text()).toContain('October 20, 2025');
    expect(wrapper.text()).toContain('October 21, 2025');
    expect(wrapper.findAll('.list-group-item-action').length).toBe(3);
  });

  it('calls createAppointment when a slot is selected and button is clicked', async () => {
    const mockDoctor = { id: '1', name: 'Dr. API Fetched', specialty: 'TDD' };
    const mockSchedule = [{ id: 99, date: '2025-10-20', start_time: '10:00:00', is_available: true }];
    apiService.getDoctor.mockResolvedValue({ data: mockDoctor });
    apiService.getSchedules.mockResolvedValue({ data: mockSchedule });
    apiService.createAppointment.mockResolvedValue({ data: {} });

    const wrapper = mount(DoctorDetail);
    await new Promise(resolve => setTimeout(resolve, 0));
    await wrapper.vm.$nextTick();

    const slotButton = wrapper.find('.list-group-item-action');
    await slotButton.trigger('click');
    await wrapper.vm.$nextTick();

    const bookingButton = wrapper.find('.btn-primary');
    await bookingButton.trigger('click');

    expect(apiService.createAppointment).toHaveBeenCalledWith(mockSchedule[0].id);
  });
});