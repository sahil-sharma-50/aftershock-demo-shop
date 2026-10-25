import { useEffect, useState } from 'react'
import { api, Stats } from '../api'

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null)
  useEffect(() => { api.dashboard().then(setStats) }, [])
  return (
    <section>
      <h1>Dashboard</h1>
      {stats && (
        <dl className="stats">
          <div><dt>Products</dt><dd>{stats.product_count}</dd></div>
          <div><dt>Units in stock</dt><dd>{stats.stock_units}</dd></div>
          <div><dt>Orders</dt><dd>{stats.order_count}</dd></div>
          <div><dt>Revenue</dt><dd>${stats.revenue.toFixed(2)}</dd></div>
        </dl>
      )}
    </section>
  )
}
