import { NavLink, Route, Routes } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import ProductsPage from './pages/ProductsPage'
import EditProductPage from './pages/EditProductPage'
import OrdersPage from './pages/OrdersPage'

export default function App() {
  return (
    <>
      <nav>
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/products">Products</NavLink>
        <NavLink to="/orders">Orders</NavLink>
      </nav>
      <main>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/products" element={<ProductsPage />} />
          <Route path="/products/:id" element={<EditProductPage />} />
          <Route path="/orders" element={<OrdersPage />} />
        </Routes>
      </main>
    </>
  )
}
