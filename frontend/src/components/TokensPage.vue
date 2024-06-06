<template>
  <v-container>
    <template v-if="isLoading">
      <v-row align="center" justify="center" class="mt-2 mb-2">
        <v-progress-circular indeterminate :size="50" :width="4"> </v-progress-circular>
      </v-row>
      <v-row align="center" justify="center" class="mt-2"> Загрузка данных </v-row>
    </template>
    <template v-if="isError">
      <v-row align="center" justify="center" class="mt-2 text-h6">
        Не удалось загрузить данные
      </v-row>
    </template>
    <template v-for="token of tokens" :key="token.id">
      <v-card class="mb-2 mx-auto" elevation="3" max-width="800">
        <v-row class="pa-5" align="center">
          <div class="font-weight-medium text-h6 ml-2">{{ token.name }}</div>
          <v-divider vertical class="mx-3"></v-divider>
          <v-spacer></v-spacer>
          <div class="text-subtitle-1 text-medium-emphasis">{{ token.token }}</div>
          <v-tooltip location="top">
            <template v-slot:activator="{ props }">
              <v-icon
                class="ml-3"
                v-bind="props"
                @mouseout="resetTooltipText"
                @click="
                  () => {
                    copyToken(token.token)
                    setTooltipText()
                  }
                "
              >
                mdi-content-copy
              </v-icon>
            </template>
            <span>{{ tooltipText }}</span>
          </v-tooltip>
        </v-row>
      </v-card>
    </template>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { useUser } from '@/user'
import { fetchAccessTokens, type AccessToken } from '@/apiFetch'

const router = useRouter()

const { getCreds } = useUser()

const tokens = ref<Array<AccessToken> | null>(null)
const isLoading = ref<boolean>(true)
const isError = ref<boolean>(false)

const tooltipText = ref<string>('Скопировать')

onMounted(() => {
  loadTokens()
})

async function loadTokens() {
  isLoading.value = true
  if (getCreds() === null) {
    router.push({ path: '/login' })
    return
  }

  try {
    tokens.value = await fetchAccessTokens()
  } catch {
    isError.value = true
  }
  isLoading.value = false
}

async function copyToken(token: string) {
  navigator.clipboard.writeText(token)
}

async function setTooltipText() {
  tooltipText.value = 'Токен скопирован!'
}

async function resetTooltipText() {
  tooltipText.value = 'Скопировать'
}
</script>
