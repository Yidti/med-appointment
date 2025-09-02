import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import DoctorDetail from '../DoctorDetail.vue';

// Mock the vue-router dependency
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
  it('should display doctor details on mount', async () => {
    const wrapper = mount(DoctorDetail);

    // Wait for the component to mount and render
    await wrapper.vm.$nextTick();

    // Assert that the doctor's name and specialty are displayed
    // These values come from the mock data inside the component itself
    expect(wrapper.text()).toContain('Dr. Alice Williams');
    expect(wrapper.text()).toContain('Cardiology');
  });
});
