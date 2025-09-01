import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Register from '../Register.vue';

describe('Register.vue', () => {
  it('renders a register form', () => {
    const wrapper = mount(Register);
    expect(wrapper.find('h2').text()).toBe('Register');
    expect(wrapper.find('form').exists()).toBe(true);
  });
});
