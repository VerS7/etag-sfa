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
            swapProductDialog('editable', item)
          }
        "
      >
        mdi-pencil
      </v-icon>
      <v-icon
        size="small"
        @click="
          () => {
            swapProductDialog('deletable', item)
          }
        "
      >
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:[`item.name`]="{ value }">
      <v-chip>
        <a class="hover-underline" :href="value">
          {{ value }}
        </a>
      </v-chip>
    </template>
    <template v-slot:[`footer.prepend`]>
      <v-btn
        class="ml-3 text-primary"
        @click="emptyProduct ? swapProductDialog('creatable', emptyProduct) : null"
        >Добавить</v-btn
      >
      <v-spacer></v-spacer>
    </template>
  </v-data-table-server>

  <v-dialog v-model="itemDialogActive" max-width="800">
    <template v-if="itemRefs.editable.value">
      <ItemEditForm
        :item="itemRefs.editable.value"
        @Submit="updateProduct"
        @Discard="itemDialogActive = !itemDialogActive"
      ></ItemEditForm>
    </template>

    <template v-if="itemRefs.deletable.value">
      <ItemDeleteForm
        :item="itemRefs.deletable.value"
        @Submit="deleteProduct"
        @Discard="itemDialogActive = !itemDialogActive"
      ></ItemDeleteForm>
    </template>

    <template v-if="itemRefs.creatable.value">
      <div>1</div>
    </template>
  </v-dialog>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref } from 'vue'

import ItemEditForm from './ItemEditForm.vue'
import ItemDeleteForm from './ItemDeleteForm.vue'

import { fetchProducts, putUpdatedProduct, deleteProductByID } from '@/apiFetch'
import { formatDate } from '@/format'
import type { Product, ProductUpdate } from '@/apiFetch'

const router = useRouter()
const userCreds: string | null = localStorage.getItem('userAuthCreds')

const search = ref<string>()

type itemAction = 'creatable' | 'deletable' | 'editable'
const itemRefs: { [key: string] } = {
  creatable: ref<Product | null>(null),
  editable: ref<Product | null>(null),
  deletable: ref<ProductUpdate | null>(null)
}

const itemDialogActive = ref<boolean>(false)

const emptyProduct = ref<ProductUpdate | null>(createEmptyProduct())

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
  { title: 'Цена, р.', key: 'price', align: 'end', sortable: false },
  { title: 'Цена по акции, р', key: 'sale_price', align: 'end', sortable: false },
  { title: 'Категория', key: 'category', align: 'end' },
  { title: 'Подкатегория', key: 'subcategory', align: 'end', sortable: false },
  { title: 'Бренд', key: 'brand', align: 'end', sortable: false },
  { title: 'Единицы', key: 'unit', align: 'end', sortable: false },
  { title: 'Производитель', key: 'producer', align: 'end', sortable: false },
  { title: 'Страна', key: 'producer_country', align: 'end', sortable: false },
  { title: 'Создано', key: 'created_at', align: 'end', sortable: false },
  { title: 'Обновлено', key: 'updated_at', align: 'end', sortable: false }
]

function createEmptyProduct(): ProductUpdate {
  return {
    name: '',
    barcode: '',
    price: 0,
    sale_price: 0,
    category: '',
    subcategory: '',
    producer: '',
    producer_country: '',
    brand: ''
  }
}

function swapProductDialog(swapTo: itemAction, item: Product | ProductUpdate) {
  for (const name in itemRefs) {
    itemRefs[name].value = name === swapTo ? item : null
  }
  itemDialogActive.value = !itemDialogActive.value
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
  itemDialogActive.value = !itemDialogActive.value

  setTimeout(() => {
    search.value = String(Date.now())
  }, 1000)
}

async function deleteProduct(productID: number) {
  if (userCreds === null) {
    router.push({ path: '/login' })
    return
  }
  try {
    deleteProductByID(userCreds, productID)
  } catch {
    return
  }
  itemDialogActive.value = !itemDialogActive.value

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
