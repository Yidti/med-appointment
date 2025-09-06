import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import Confirmation from '../Confirmation.vue';
import { useRoute } from 'vue-router';

// Mock the vue-router
vi.mock('vue-router', () => ({
  useRoute: vi.fn(),
  useRouter: vi.fn(() => ({ push: vi.fn() })),
}));

describe('Confirmation.vue', () => {
  it('renders appointment details from route state', async () => {
    // Mock route state
    const appointment = {
      doctor_name: 'Dr. Feelgood',
      doctor_specialty: 'General Practice',
      schedule_date: '2025-12-25',
      schedule_start_time: '09:00:00',
    };
    history.pushState({ appointment }, '');

    useRoute.mockReturnValue({
      path: '/booking/confirmation',
      name: 'Confirmation',
      params: {},
      query: {},
      hash: '',
      fullPath: '/booking/confirmation',
      matched: [],
      meta: {},
      redirectedFrom: undefined,
    });

    // Mount the component
    const wrapper = mount(Confirmation);

    // Wait for the component to update
    await new Promise(resolve => setTimeout(resolve, 0));

    // Assert appointment details
    expect(wrapper.text()).toContain('預約成功');
    expect(wrapper.text()).toContain('Dr. Feelgood');
    expect(wrapper.text()).toContain('General Practice');
  });
});
