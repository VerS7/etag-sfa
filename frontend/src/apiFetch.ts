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
  price: number | string
  sale_price: number | null
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
  price: number | null
  sale_price: number | null
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

const API_URL: string = 'http://127.0.0.1:8000/api'

export function getAuthCreds(user: User): string {
  return 'Basic ' + btoa(`${user.username}:${user.password}`)
}

export async function fetchUser(authCreds: string): Promise<UserResponse> {
  const response = await fetch(API_URL + '/login', {
    method: 'GET',
    headers: {
      Authorization: authCreds
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

export async function fetchProducts(
  authCreds: string,
  page: number,
  pageSize: number
): Promise<ProductPage> {
  const response = await fetch(API_URL + `/product/?page=${page}&size=${pageSize}`, {
    method: 'GET',
    headers: {
      Authorization: authCreds
    }
  })

  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }

  return response.json()
}

export async function putUpdatedProduct(
  authCreds: string,
  product: ProductUpdate,
  productID: number
): Promise<void> {
  const response = await fetch(API_URL + `/product/${productID}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      Authorization: authCreds
    },
    body: JSON.stringify(product)
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
}

export async function deleteProductByID(authCreds: string, productID: number): Promise<void> {
  const response = await fetch(API_URL + `/product/${productID}/`, {
    method: 'DELETE',
    headers: {
      Authorization: authCreds
    }
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
}

export async function createNewProduct(authCreds: string, product: ProductUpdate): Promise<void> {
  const response = await fetch(API_URL + `/product/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: authCreds
    },
    body: JSON.stringify(product)
  })
  if (!response.ok) {
    throw { error: new Error(`${response.statusText}`), code: response.status }
  }
}
