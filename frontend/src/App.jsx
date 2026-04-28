import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Cameras from './pages/Cameras'
import Layout from './components/Layout'

function RotaProtegida({ children }) {
  const { usuario } = useAuth()
  if (!usuario) {
    return <Navigate to="/login" replace />
  }
  return <Layout>{children}</Layout>
}

function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <RotaProtegida>
            <div>
              <h1>Dashboard</h1>
            </div>
          </RotaProtegida>
        }
      />
      <Route
        path="/cameras"
        element={
          <RotaProtegida>
            <Cameras />
          </RotaProtegida>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App