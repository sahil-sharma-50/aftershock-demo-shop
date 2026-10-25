import { FormEvent, useCallback, useEffect, useState } from 'react'
import { api, ApiError, Order, Product } from '../api'

export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [productId, setProductId] = useState('')
  const [quantity, setQuantity] = useState('1')
  const [error, setError] = useState('')

  const load = useCallback(async () => {
    const [o, p] = await Promise.all([api.orders(), api.products()])
    setOrders(o); setProducts(p)
    setProductId((cur) => cur || (p[0] ? String(p[0].id) : ''))
  }, [])
  useEffect(() => { load() }, [load])

  async function place(e: FormEvent) {
    e.preventDefault()
    setError('')
    try {
      await api.createOrder(Number(productId), Number(quantity))
      await load()
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) setError('Not enough stock')
      else throw err
    }
  }

  return (
    <section>
      <h1>Orders</h1>
      <h2>New order</h2>
      <form onSubmit={place}>
        <div className="field"><label htmlFor="product">Product</label>
          <select id="product" value={productId} onChange={(e) => setProductId(e.target.value)}>
            {products.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
          </select></div>
        <div className="field"><label htmlFor="quantity">Quantity</label>
          <input id="quantity" type="number" min="1" required value={quantity} onChange={(e) => setQuantity(e.target.value)} /></div>
        <button type="submit">Place order</button>
        {error && <span className="error" role="alert">{error}</span>}
      </form>
      <p><a href="/api/orders/export.csv" download>Export CSV</a></p>
      <table>
        <thead><tr><th>Order</th><th>Product</th><th>Quantity</th><th>Total</th><th>Placed</th></tr></thead>
        <tbody>
          {orders.map((o) => (
            <tr key={o.id}>
              <td>{o.id}</td><td>{o.product_name}</td><td>{o.quantity}</td>
              <td>${o.total.toFixed(2)}</td><td>{new Date(o.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
