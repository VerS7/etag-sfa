<style scoped></style>
<template>
  <v-data-table-server
    dense
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :items="items"
    :items-length="totalItems"
    :loading="loading"
    :search="search"
    item-value="name"
    @update:options="loadItems"
  ></v-data-table-server>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

import { fetchProducts } from '@/apiFetch'

const router = useRouter()
const userCreds: string | null = localStorage.getItem('userAuthCreds')

const search = ref()
const loading = ref(false)
const totalItems = ref(0)
const items = ref()
const itemsPerPage = ref(15)

const headers = [
  { title: 'ID', key: 'id', align: 'end' },
  { title: 'Название', key: 'name', align: 'end' },
  { title: 'Штрих-код', key: 'barcode', align: 'end' },
  { title: 'Цена, р.', key: 'price', align: 'end' },
  { title: 'Цена по акции, р', key: 'sale_price', align: 'end' },
  { title: 'Категория', key: 'category', align: 'end' },
  { title: 'Подкатегория', key: 'subcategory', align: 'end' },
  { title: 'Бренд', key: 'brand', align: 'end' },
  { title: 'Единицы измерения', key: 'unit', align: 'end' },
  { title: 'Производитель', key: 'producer', align: 'end' },
  { title: 'Страна', key: 'producer_country', align: 'end' },
  { title: 'Создано', key: 'created_at', align: 'end' },
  { title: 'Обновлено', key: 'updated_at', align: 'end' }
]

async function loadItems() {
  if (userCreds === null) {
    router.push({ path: '/login' })
    return
  }
  const productPage = await fetchProducts(userCreds, 1, itemsPerPage.value)
  items.value = productPage.items
  if (productPage.total !== null) {
    totalItems.value = productPage.total
  }
}
</script>
