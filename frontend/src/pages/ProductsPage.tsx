import { FormEvent, useCallback, useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api, Product } from '../api'

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [search, setSearch] = useState('')
  const [name, setName] = useState('')
  const [price, setPrice] = useState('')
  const [stock, setStock] = useState('')

  const load = useCallback(() => api.products(search).then(setProducts), [search])
  useEffect(() => { load() }, [load])

  async function add(e: FormEvent) {
    e.preventDefault()
    await api.createProduct({ name, price: Number(price), stock: Number(stock || 0) })
    setName(''); setPrice(''); setStock('')
    load()
  }

  return (
    <section>
      <h1>Products</h1>
      <div className="field">
        <label htmlFor="search">Search products</label>
        <input id="search" type="search" value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>
      <table>
        <thead><tr><th>Name</th><th>Price</th><th>Stock</th><th></th></tr></thead>
        <tbody>
          {products.map((p) => (
            <tr key={p.id}>
              <td>{p.name}</td>
              <td>${p.price.toFixed(2)}</td>
              <td>{p.stock}</td>
              <td><Link to={`/products/${p.id}`}>Edit</Link></td>
            </tr>
          ))}
        </tbody>
      </table>
      <h2>Add product</h2>
      <form onSubmit={add}>
        <div className="field"><label htmlFor="new-name">Name</label>
          <input id="new-name" required value={name} onChange={(e) => setName(e.target.value)} /></div>
        <div className="field"><label htmlFor="new-price">Price</label>
          <input id="new-price" type="number" step="0.01" min="0" required value={price} onChange={(e) => setPrice(e.target.value)} /></div>
        <div className="field"><label htmlFor="new-stock">Stock</label>
          <input id="new-stock" type="number" min="0" required value={stock} onChange={(e) => setStock(e.target.value)} /></div>
        <button type="submit">Add product</button>
      </form>
    </section>
  )
}
