// Vue
import { createApp } from 'vue'
import App from './App.vue'

// Router
import { createRouter, createWebHistory } from 'vue-router'

// Vuetify
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Components
import MainPage from './components/MainPage.vue'
import LoginForm from './components/LoginForm.vue'

const vuetify = createVuetify({
  components,
  directives
})

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Home', component: MainPage },
    {
      path: '/login',
      name: 'Login',
      component: LoginForm
    }
  ]
})

createApp(App).use(vuetify).use(router).mount('#app')
