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
    :search="search"
    :density="'comfortable'"
    :itemsPerPageText="'Отобразить элементов:'"
    :no-data-text="'Не удалось загрузить данные.'"
    :loading-text="'Загрузка данных...'"
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
      <v-icon
        ref="editItemActivator"
        class="me-2"
        size="small"
        @click="
          () => {
            editableItem = item
            editItemActive = !editItemActive
          }
        "
      >
        mdi-pencil
      </v-icon>
      <v-icon size="small" @click="console.log(item)"> mdi-delete </v-icon>
    </template>

    <template v-slot:[`item.name`]="{ value }">
      <v-chip>
        <a class="hover-underline" :href="value">
          {{ value }}
        </a>
      </v-chip>
    </template>
  </v-data-table-server>

  <v-dialog v-model="editItemActive" max-width="800">
    <template v-if="editableItem">
      <ItemEditForm
        :item="editableItem"
        @Submit="updateProduct"
        @Discard="editItemActive = !editItemActive"
      ></ItemEditForm>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

import ItemEditForm from './ItemEditForm.vue'

import { fetchProducts, putUpdatedProduct } from '@/apiFetch'
import { formatDate } from '@/format'
import type { Product, ProductUpdate } from '@/apiFetch'

const router = useRouter()
const userCreds: string | null = localStorage.getItem('userAuthCreds')

const search = ref<string>()
const editItemActive = ref<boolean>(false)
const editableItem = ref<Product | null>(null)

const loading = ref<boolean>(false)
const totalItems = ref<number>(0)
const items = ref<Array<Product>>()
const itemsPerPage = ref<number>(15)
const page = ref<number>(1)

interface ProductDataTableHeader {
  title: string
  key: string
  align: 'start' | 'end' | 'center'
  sortable?: boolean
}

interface paginationOptions {
  page: number
  itemsPerPage: number
  sortBy: string
}

const headers: ProductDataTableHeader[] = [
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

async function updateProduct(product: ProductUpdate, productID: number) {
  if (userCreds === null) {
    router.push({ path: '/login' })
    return
  }

  try {
    putUpdatedProduct(userCreds, product, productID)
  } catch {
    return
  }
  editItemActive.value = !editItemActive.value

  setTimeout(() => {
    search.value = String(Date.now())
  }, 1000)
}

async function loadItems(options: paginationOptions) {
  if (userCreds === null) {
    router.push({ path: '/login' })
    return
  }

  let productPage = null

  loading.value = true

  try {
    productPage = await fetchProducts(userCreds, options.page, options.itemsPerPage)
  } catch {
    loading.value = false
    return
  }

  page.value = options.page

  items.value = productPage.items.map((element) => {
    return {
      ...element,
      created_at: formatDate(element.created_at),
      updated_at: element.updated_at ? formatDate(element.updated_at) : null
    }
  })

  loading.value = false

  if (productPage.total !== null) {
    totalItems.value = productPage.total
  }
}
</script>
