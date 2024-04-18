<template>
  <v-card v-if="item">
    <v-card-title class="font-weight-bold">Редактирование</v-card-title>
    <v-divider></v-divider>
    <v-form ref="itemForm">
      <v-card-text>
        <div class="text-subtitle-2 text-medium-emphasis mb-2 ml-1">Товар</div>
        <v-row dense>
          <v-col cols="12" md="6" class="mb-2">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.name"
              label="Название"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6" class="mb-2">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.category"
              label="Категория"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.barcode"
              label="Штрих-код"
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.subcategory"
              label="Подкатегория"
            ></v-text-field>
          </v-col>
        </v-row>
        <div class="text-subtitle-2 text-medium-emphasis mb-2 ml-1 mt-2">Цена</div>
        <v-row dense>
          <v-col cols="12" md="6">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.price"
              type="number"
              label="Цена"
              suffix="руб."
              hide-spin-buttons
              required
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.sale_price"
              type="number"
              label="Цена по акции"
              suffix="руб."
              hide-spin-buttons
            ></v-text-field>
          </v-col>
        </v-row>
        <div class="text-subtitle-2 text-medium-emphasis mb-2 ml-1 mt-2">Производитель</div>
        <v-row dense>
          <v-col cols="12" md="4">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.producer"
              label="Производитель"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="4">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.brand"
              label="Бренд"
            ></v-text-field> </v-col
          ><v-col cols="12" md="4">
            <v-text-field
              hide-details="auto"
              density="compact"
              variant="outlined"
              v-model="newItem.producer_country"
              label="Страна"
            ></v-text-field>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <div v-if="!formValidity" class="text-subtitle-2 text-red ml-3">
          Данные введены некорректно.
        </div>
        <v-spacer></v-spacer>
        <v-btn @click="emits('discard')" variant="text" color="red"> Закрыть </v-btn>
        <v-btn @click="validateForm()" variant="text" color="primary"> Сохранить </v-btn>
      </v-card-actions>
    </v-form>
  </v-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { VForm } from 'vuetify/components'

import type { Product, ProductUpdate } from '@/apiFetch'
import { formatProduct, productToProductUpdate } from '@/format'

const props = defineProps<{
  item: Product
}>()

let productID = props.item.id

let newItem = ref<ProductUpdate>(productToProductUpdate(props.item))

const emits = defineEmits<{
  (e: 'submit', data: ProductUpdate, productID: number): void
  (e: 'discard'): void
}>()

const itemForm = ref<VForm | null>(null)
const formValidity = ref<boolean>(true)

async function validateForm() {
  if (!itemForm.value) {
    return
  }

  const { valid } = await itemForm.value.validate()

  if (!valid) {
    formValidity.value = false
    return
  }
  emits('submit', formatProduct(newItem.value), productID)
}
</script>
