<template>
  <v-container fluid class="mb-10" dense>
    <v-app-bar color="light-green" elevation="5" dense>
      <v-btn height="70%" class="ml-5" :prepend-icon="'mdi-tag'" @click="router.push({ path: '/' })"
        >Продукты</v-btn
      >
      <v-btn
        height="70%"
        class="ml-5"
        :prepend-icon="'mdi-account-group'"
        @click="router.push({ path: '/users' })"
        >Пользователи</v-btn
      >
      <v-btn
        v-if="user?.role === 'admin'"
        height="70%"
        class="ml-5"
        :prepend-icon="'mdi-shield-crown'"
        @click="router.push({ path: '/admin' })"
        >Админ-панель</v-btn
      >
      <v-spacer></v-spacer>
      <v-menu :location="'center'">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" height="70%" :prepend-icon="'mdi-account-circle'"
            >Пользователь</v-btn
          >
        </template>
        <v-card>
          <v-list>
            <v-list-item
              prepend-icon="mdi-account-circle"
              :subtitle="user?.role === 'admin' ? 'Администратор' : 'Пользователь'"
              :title="user?.name"
            >
            </v-list-item>
          </v-list>
          <v-divider></v-divider>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="red"
              variant="text"
              @click="
                () => {
                  userLogout()
                  router.push({ path: '/login' })
                }
              "
            >
              Выйти
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-menu>
    </v-app-bar>
  </v-container>
  <ProductTable> </ProductTable>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

import ProductTable from './ProductTable.vue'

import { getUser, getUserCreds, userLogout } from '@/user'
import type { UserResponse } from '@/apiFetch'

const router = useRouter()

const user = ref<UserResponse | null>(getUser())
const userCreds: string | null = getUserCreds()

if (!userCreds) {
  router.push({ path: '/login' })
}
</script>
