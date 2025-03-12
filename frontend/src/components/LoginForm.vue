<template>
  <div class="mt-10">
    <v-img class="mx-auto my-6" max-width="250" src="assets/Logo.png"></v-img>

    <v-card class="mx-auto pa-5 pb-5" elevation="5" max-width="400" rounded="lg">
      <v-form ref="form">
        <div class="text-subtitle-1 text-medium-emphasis">Имя пользователя</div>
        <v-text-field
          v-model="username"
          :rules="[(v: string) => !!v || 'Отсутствует имя пользователя.']"
          density="compact"
          placeholder="Введите имя пользователя"
          variant="outlined"
          required
        ></v-text-field>

        <div class="text-subtitle-1 text-medium-emphasis">Пароль</div>
        <v-text-field
          :append-inner-icon="visible ? 'mdi-eye' : 'mdi-eye-closed'"
          :type="visible ? 'text' : 'password'"
          v-model="password"
          :rules="[(v: string) => !!v || 'Отсутствует пароль.']"
          density="compact"
          placeholder="Введите пароль"
          variant="outlined"
          @click:append-inner="visible = !visible"
          required
        ></v-text-field>
      </v-form>
      <div class="mt-1 text-subtitle-2 text-center text-red" color="">
        <div v-if="unauth">Неверное имя пользователя или пароль.</div>
        <div v-if="fetchErr">Не удалось получить данные.</div>
      </div>
      <v-btn
        class="mt-1"
        block
        :color="unauth || fetchErr ? 'red' : 'green'"
        size="large"
        variant="tonal"
        @click="submit"
        >Войти</v-btn
      >
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { VForm } from 'vuetify/components'

import { useUser } from '@/user'
import { useRouter } from 'vue-router'

const form = ref<VForm | null>(null)

const router = useRouter()

const username = ref('')
const password = ref('')

const visible = ref(false)
const fetchErr = ref(false)
const unauth = ref(false)

const { login } = useUser()

async function submit(): Promise<void> {
  fetchErr.value = false
  unauth.value = false

  if (!form.value) {
    return
  }
  const { valid } = await form.value.validate()

  if (!valid) {
    return
  }

  try {
    await login({ username: username.value, password: password.value })
  } catch (error) {
    if (typeof error !== 'object' || error === null || !('code' in error)) {
      return
    }
    error.code == 401 ? (unauth.value = true) : (fetchErr.value = true)
    return
  }
  router.push('/')
}
</script>
