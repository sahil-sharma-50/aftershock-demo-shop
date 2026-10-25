import { FormEvent, useCallback, useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api, ApiError, Product } from '../api'

export default function EditProductPage() {
  const { id = '' } = useParams()
  const [product, setProduct] = useState<Product | null>(null)
  const [name, setName] = useState('')
  const [price, setPrice] = useState('')
  const [saved, setSaved] = useState(false)
  const [delta, setDelta] = useState('')
  const [stockError, setStockError] = useState('')

  const load = useCallback(async () => {
    const p = await api.product(id)
    setProduct(p); setName(p.name); setPrice(String(p.price))
  }, [id])
  useEffect(() => { load() }, [load])

  async function save(e: FormEvent) {
    e.preventDefault()
    setSaved(false)
    await api.updateProduct(id, { name, price: Number(price) })
    await load()
    setSaved(true)
  }

  async function adjust(e: FormEvent) {
    e.preventDefault()
    setStockError('')
    try {
      const p = await api.adjustStock(id, Number(delta))
      setProduct(p); setDelta('')
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) setStockError('Not enough stock')
      else throw err
    }
  }

  if (!product) return <section><h1>Edit product</h1></section>

  return (
    <section>
      <h1>Edit product</h1>
      <form onSubmit={save}>
        <div className="field"><label htmlFor="name">Name</label>
          <input id="name" required value={name} onChange={(e) => setName(e.target.value)} /></div>
        <div className="field"><label htmlFor="price">Price</label>
          <input id="price" type="number" step="0.01" min="0" required value={price} onChange={(e) => setPrice(e.target.value)} /></div>
        <button type="submit">Save</button>
        {saved && <span className="ok" role="status">Saved</span>}
      </form>
      <h2>Adjust stock</h2>
      <p>Current stock: {product.stock}</p>
      <form onSubmit={adjust}>
        <div className="field"><label htmlFor="delta">Quantity change</label>
          <input id="delta" type="number" required value={delta} onChange={(e) => setDelta(e.target.value)} /></div>
        <button type="submit">Apply</button>
        {stockError && <span className="error" role="alert">{stockError}</span>}
      </form>
    </section>
  )
}
