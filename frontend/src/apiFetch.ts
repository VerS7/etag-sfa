import { useUser } from '@/user'

export interface User {
  username: string
  password: string
}

export interface UserResponse {
  role: string
  name: string
  hashed: string
}

export interface Product {
  id: number
  name: string
  barcode: string
  price: string
  sale_price: string | null
  category: string | null
  subcategory: string | null
  producer: string | null
  producer_country: string | null
  brand: string | null
  unit: string | null
  created_at: string
  updated_at: string | null
}

export interface ProductUpdate {
  name: string | null
  barcode: string | null
  price: string | null
  sale_price: string | null
  category: string | null
  subcategory: string | null
  unit: string | null
  producer: string | null
  producer_country: string | null
  brand: string | null
}

export interface ProductPage {
  items: Array<Product>
  total: number | null
  page: number | null
  size: number | null
  pages: number | null
}

export interface AccessToken {
  id: number
  name: string
  token: string
}

const API_URL: string = 'http://127.0.0.1:8000/api'

const { getCreds } = useUser()

export async function fetchUser(userCreds: string): Promise<UserResponse> {
  const response = await fetch(API_URL + '/login', {
    method: 'GET',
    headers: {
      Authorization: userCreds
    }
  })

  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }

  return response.json().then((data) => ({
    name: data.username,
    hashed: data.hashed_password,
    role: data.role
  }))
}

export async function fetchProducts(page: number, pageSize: number): Promise<ProductPage> {
  const creds = getCreds()
  if (creds === null) {
    throw new Error('User credentials not found!')
  }

  const response = await fetch(API_URL + `/product/?page=${page}&size=${pageSize}`, {
    method: 'GET',
    headers: {
      Authorization: creds
    }
  })

  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }

  return response.json()
}

export async function putUpdatedProduct(product: ProductUpdate, productID: number): Promise<void> {
  const creds = getCreds()
  if (creds === null) {
    throw new Error('User credentials not found!')
  }

  const response = await fetch(API_URL + `/product/${productID}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: creds
    },
    body: JSON.stringify(product)
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
}

export async function deleteProductByID(productID: number): Promise<void> {
  const creds = getCreds()
  if (creds === null) {
    throw new Error('User credentials not found!')
  }

  const response = await fetch(API_URL + `/product/${productID}/`, {
    method: 'DELETE',
    headers: {
      Authorization: creds
    }
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
}

export async function createNewProduct(product: ProductUpdate): Promise<void> {
  const creds = getCreds()
  if (creds === null) {
    throw new Error('User credentials not found!')
  }

  const response = await fetch(API_URL + `/product/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: creds
    },
    body: JSON.stringify(product)
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
}

export async function getProductImage(productID: number): Promise<Blob> {
  const creds = getCreds()
  if (creds === null) {
    throw new Error('User credentials not found!')
  }

  const response = await fetch(API_URL + `/product/image/${productID}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'image/png',
      Authorization: creds
    }
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
  return response.blob()
}

export async function fetchAccessTokens(): Promise<Array<AccessToken>> {
  const creds = getCreds()
  if (creds === null) {
    throw new Error('User credentials not found!')
  }

  const response = await fetch(API_URL + `/token`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: creds
    }
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
  return response.json()
}
