<template>
  <v-card>
    <v-card-title class="text-h5 mt-2 mb-2 font-weight-bold">{{ item.name }}</v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <div class="mb-5">
        <v-row><span class="text-subtitle-2 text-medium-emphasis">Штрих-код</span></v-row>
        <v-row>
          <span class="ml-2">{{ item.barcode }}</span>
        </v-row>
      </div>
      <div class="mb-5">
        <v-row><span class="text-subtitle-2 text-medium-emphasis">Цена</span></v-row>
        <v-row>
          <span class="ml-2 mr-1">{{ String(item.price).replace(/.0*$/, '') }}</span
          ><span>₽</span>
        </v-row>
      </div>
      <div class="mb-5" v-if="item.sale_price">
        <v-row><span class="text-subtitle-2 text-medium-emphasis">Цена по акции</span></v-row>
        <v-row>
          <span class="ml-2 mr-1">{{ String(item.sale_price).replace(/.0*$/, '') }}</span
          ><span>₽</span>
        </v-row>
      </div>
      <div class="mb-5" v-if="item.unit">
        <v-row><span class="text-subtitle-2 text-medium-emphasis">Единицы измерения</span></v-row>
        <v-row>
          <span class="ml-2 mr-1">{{ item.unit }}</span>
        </v-row>
      </div>
      <div class="mb-5" v-if="item.category">
        <v-row><span class="text-subtitle-2 text-medium-emphasis">Категория</span></v-row>
        <v-row>
          <span class="ml-2 mr-1">{{ item.category }}</span>
          <span v-if="item.subcategory"> / {{ item.subcategory }}</span>
        </v-row>
      </div>
      <div class="mb-5" v-if="item.brand || item.producer_country">
        <v-row><span class="text-subtitle-2 text-medium-emphasis">Производитель</span></v-row>
        <v-row v-if="item.producer">
          <span class="ml-2">{{ item.brand }} </span>
          <span class="ml-1" v-if="item.producer"> / {{ item.producer }}</span>
          <span class="ml-1" v-if="item.producer_country"> / {{ item.producer_country }}</span>
        </v-row>
        <v-row v-else>
          <span class="ml-2">{{ item.producer_country }} </span>
        </v-row>
      </div>
    </v-card-text>
    <v-expansion-panels>
      <v-expansion-panel>
        <v-expansion-panel-title> Предпросмотр ценника </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row no-gutters>
            <v-select
              :items="imageOptions"
              v-model="selectedOption"
              label="Вариант"
              variant="outlined"
              density="compact"
            ></v-select>
            <v-btn class="text-primary ml-5" @click="loadProductImage(selectedOption)">
              Создать
            </v-btn>
          </v-row>
          <v-row>
            <v-img v-if="imageURL" :src="imageURL" :max-width="300" class="mb-2 mx-auto">
              <template v-slot:placeholder>
                <div class="d-flex align-center justify-center fill-height">
                  <v-progress-circular color="grey-lighten-4" indeterminate></v-progress-circular>
                </div>
              </template>
            </v-img>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<script setup lang="ts">
import { getProductImage, type Product } from '@/apiFetch'
import { ref } from 'vue'

import { useUser } from '@/user'

const { check } = useUser()

const props = defineProps<{
  item: Product
}>()

const imageOptions = ref<[string]>(['default'])
const imageURL = ref<string | null>(null)
const selectedOption = ref<string | null>(null)

async function loadProductImage(option: string | null) {
  if (!check() || !option) {
    return
  }
  const image = await getProductImage(props.item.id)
  imageURL.value = URL.createObjectURL(image)
}
</script>
