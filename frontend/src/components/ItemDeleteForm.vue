<template>
  <v-card v-if="item" max-width="auto">
    <v-card-title class="font-weight-bold">Удаление</v-card-title>
    <v-divider></v-divider>
    <v-card-text class="mx-auto"
      ><div class="ml-2">
        <p class="text-weight-medium text-h6">
          Вы действительно хотите удалить
          <v-chip class="font-weight-bold text-subtitle-2">
            {{ item.name }}
          </v-chip>
          ?
        </p>
      </div>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions class="mx-auto">
      <v-btn @click="emits('discard')" variant="text" color="primary"> Закрыть </v-btn>
      <v-btn @click="emits('submit', item.id)" variant="text" color="red"> Удалить </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
import type { Product } from '@/apiFetch'

defineProps<{ item: Product }>()

const emits = defineEmits<{
  (e: 'submit', productID: number): void
  (e: 'discard'): void
}>()
</script>
