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
  price: string | null
  sale_price: string | null
  category: string | null
  producer: string | null
  producer_country: string | null
  created_at: string
  updated_at: string | null
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
