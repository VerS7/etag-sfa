import type { Product, ProductUpdate } from './apiFetch'

export function formatProduct(product: Product | ProductUpdate): ProductUpdate {
  return {
    ...product,
    price:
      typeof product.price === 'string'
        ? parseFloat(product.price).toFixed(2).toString()
        : product.price,
    sale_price:
      typeof product.sale_price === 'string'
        ? parseFloat(product.sale_price).toFixed(2).toString()
        : product.sale_price
  }
}

export function productToProductUpdate(product: Product): ProductUpdate {
  return Object.fromEntries(
    Object.entries(product).filter(([key]) => !['id', 'created_at', 'updated_at'].includes(key))
  ) as ProductUpdate
}

export function formatDate(date: string): string {
  const d = new Date(date)
  return `${formatUnit(d.getDate())}.${formatUnit(d.getMonth())}.${formatUnit(d.getFullYear())} ${formatUnit(d.getHours())}:${formatUnit(d.getMinutes())}`
}

function formatUnit(unit: number): string {
  const u = unit.toString()
  return u.length < 2 ? '0' + u : u
}
