<style scoped>
.hover-underline {
  text-decoration: none;
  display: inline-block;
  position: relative;
  color: #0087ca;
}
.hover-underline:after {
  content: '';
  position: absolute;
  width: 100%;
  transform: scaleX(0);
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: #0087ca;
  transform-origin: bottom right;
  transition: transform 0.25s ease-out;
}

.hover-underline:hover:after {
  transform: scaleX(1);
  transform-origin: bottom left;
}
</style>

<template>
  <v-data-table-server
    v-model:items-per-page="itemsPerPage"
    :headers="headers"
    :page="page"
    :items="items"
    :items-length="totalItems"
    :loading="loading"
    :density="'comfortable'"
    :itemsPerPageText="'Отобразить элементов:'"
    :page-text="pageText()"
    :items-per-page-options="[
      { value: 15, title: '15' },
      { value: 30, title: '30' },
      { value: 50, title: '50' },
      { value: 100, title: '100' }
    ]"
    item-value="name"
    @update:options="loadItems"
  >
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon class="me-2" size="small" @click="editItem(item)"> mdi-pencil </v-icon>
      <v-icon size="small" @click="deleteItem(item)"> mdi-delete </v-icon>
    </template>

    <template v-slot:[`item.name`]="{ value }">
      <v-chip>
        <a class="hover-underline" :href="value">
          {{ value }}
        </a>
      </v-chip>
    </template>
  </v-data-table-server>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

import { fetchProducts } from '@/apiFetch'
import { formatDate } from '@/format'
import type { Product } from '@/apiFetch'

const router = useRouter()
const userCreds: string | null = localStorage.getItem('userAuthCreds')

const loading = ref<boolean>(false)
const totalItems = ref<number>(0)
const items = ref<Array<Product>>()
const itemsPerPage = ref<number>(15)
const page = ref<number>(1)

const headers = [
  { title: 'Действие', key: 'actions', align: 'end', sortable: false },
  { title: 'ID', key: 'id', align: 'end', sortable: false },
  { title: 'Название', key: 'name', align: 'end', sortable: false },
  { title: 'Штрих-код', key: 'barcode', align: 'end', sortable: false },
  { title: 'Цена, р.', key: 'price', align: 'end' },
  { title: 'Цена по акции, р', key: 'sale_price', align: 'end' },
  { title: 'Категория', key: 'category', align: 'end' },
  { title: 'Подкатегория', key: 'subcategory', align: 'end' },
  { title: 'Бренд', key: 'brand', align: 'end' },
  { title: 'Единицы', key: 'unit', align: 'end' },
  { title: 'Производитель', key: 'producer', align: 'end' },
  { title: 'Страна', key: 'producer_country', align: 'end' },
  { title: 'Создано', key: 'created_at', align: 'end' },
  { title: 'Обновлено', key: 'updated_at', align: 'end' }
]

interface paginationOptions {
  page: number
  itemsPerPage: number
  sortBy: string
}

function pageText(): string {
  const p = page.value
  const ipt = itemsPerPage.value
  const t = totalItems.value

  if (!p || !ipt) {
    return ''
  }

  const start = (p - 1) * ipt
  const end = Math.min(start + ipt - 1, t - 1)

  return `${start + 1}-${end + 1} из ${t}`
}

async function loadItems(options: paginationOptions) {
  if (userCreds === null) {
    router.push({ path: '/login' })
    return
  }
  loading.value = true
  page.value = options.page
  const productPage = await fetchProducts(userCreds, options.page, options.itemsPerPage)

  items.value = productPage.items.map((element) => {
    loading.value = false
    return {
      ...element,
      created_at: formatDate(element.created_at),
      updated_at: element.updated_at ? formatDate(element.updated_at) : null
    }
  })

  if (productPage.total !== null) {
    totalItems.value = productPage.total
  }
}
</script>
