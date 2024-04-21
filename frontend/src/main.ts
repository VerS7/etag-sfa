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
import ProductTable from './components/ProductTablePage.vue'
import UsersPage from './components/TokensPage.vue'
import AdminPanelPage from './components/AdminPanelPage.vue'

const vuetify = createVuetify({
  components,
  directives
})

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: LoginForm
    },
    {
      path: '/',
      name: 'Home',
      component: MainPage,
      children: [
        {
          path: '/products',
          name: 'Products',
          component: ProductTable
        },
        {
          path: '/tokens',
          name: 'Tokens',
          component: UsersPage
        },
        {
          path: '/admin',
          name: 'Admin-panel',
          component: AdminPanelPage
        }
      ]
    }
  ]
})

createApp(App).use(vuetify).use(router).mount('#app')
