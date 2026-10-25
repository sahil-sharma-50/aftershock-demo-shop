export interface Product { id: number; name: string; price: number; stock: number }
export interface Order { id: number; product_id: number; product_name: string; quantity: number; total: number; created_at: string }
export interface Stats { product_count: number; stock_units: number; order_count: number; revenue: number }

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message) }
}

async function req<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(path, {
    ...init,
    headers: init?.body ? { 'Content-Type': 'application/json' } : undefined,
  })
  if (!res.ok) throw new ApiError(res.status, await res.text())
  return res.json() as Promise<T>
}

const json = (method: string, body: unknown): RequestInit => ({ method, body: JSON.stringify(body) })

export const api = {
  dashboard: () => req<Stats>('/api/dashboard'),
  products: (q?: string) => req<Product[]>('/api/products' + (q ? `?q=${encodeURIComponent(q)}` : '')),
  product: (id: string) => req<Product>(`/api/products/${id}`),
  createProduct: (p: { name: string; price: number; stock: number }) => req<Product>('/api/products', json('POST', p)),
  updateProduct: (id: string, p: { name: string; price: number }) => req<Product>(`/api/products/${id}`, json('PUT', p)),
  adjustStock: (id: string, delta: number) => req<Product>(`/api/products/${id}/stock`, json('POST', { delta })),
  orders: () => req<Order[]>('/api/orders'),
  createOrder: (product_id: number, quantity: number) => req<Order>('/api/orders', json('POST', { product_id, quantity })),
}
