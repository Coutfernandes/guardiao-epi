import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Cameras from './pages/Cameras'
import Alertas from './pages/Alertas'
import Relatorios from './pages/Relatorios'
import ConfiguracaoEPIs from './pages/ConfiguracaoEPIs'
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
            <Dashboard />
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
      <Route
        path="/alertas"
        element={
          <RotaProtegida>
            <Alertas />
          </RotaProtegida>
        }
      />
      <Route
        path="/relatorios"
        element={
          <RotaProtegida>
            <Relatorios />
          </RotaProtegida>
        }
      />
      <Route
        path="/configuracao-epis"
        element={
          <RotaProtegida>
            <ConfiguracaoEPIs />
          </RotaProtegida>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App