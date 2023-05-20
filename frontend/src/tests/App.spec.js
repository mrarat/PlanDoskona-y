import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '../App.vue'

import ResizeObserver from 'resize-observer-polyfill';
global.ResizeObserver = ResizeObserver;

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

function mountWithVuetify (component, options) {
  const vuetify = createVuetify({
    components,
    directives,
  })
  
  return mount(component, {
      ...options,
      global: {
          plugins: [vuetify]
      },
  })
}

describe('some test', () => {
  it('initializes message_sent properly', () => {
    const wrapper = mountWithVuetify(App)
    expect(wrapper.vm.message_sent).toBe('')
  })
})
