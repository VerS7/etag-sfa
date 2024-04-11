<style scoped></style>

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
        >Админ</v-btn
      >
      <v-spacer></v-spacer>
      <v-btn
        height="70%"
        :prepend-icon="'mdi-account-circle'"
        @click="
          () => {
            userLogout()
            router.push({ path: '/login' })
          }
        "
        >Пользователь</v-btn
      >
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
