import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('some test', () => {
  it('initializes message_sent properly', () => {
    const wrapper = mount(App)
    expect(wrapper.vm.message_sent).toBe('')
  })
})
