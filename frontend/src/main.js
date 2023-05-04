import { createApp } from 'vue'
import App from './App.vue'

import './assets/main.css'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import Multiselect from 'vue-multiselect'

const vuetify = createVuetify({
    components,
    directives,
})

const app = createApp(App).component('multiselect', Multiselect)
app.use(vuetify)

app.mount('#app')
