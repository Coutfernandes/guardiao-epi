import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { Home, Camera, Bell, FileText, Settings, LogOut } from 'lucide-react'
import logo from '../assets/logo.svg'

const menuItems = [
  { path: '/', icon: Home, label: 'Inicio' },
  { path: '/cameras', icon: Camera, label: 'Cameras' },
  { path: '/alertas', icon: Bell, label: 'Alertas' },
  { path: '/relatorios', icon: FileText, label: 'Relatorios' },
  { path: '/configuracao-epis', icon: Settings, label: 'Configuracao EPIs' },
]

export default function Layout({ children }) {
  const { usuario, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh', backgroundColor: '#F8FAFC' }}>
      <aside style={{
        width: '220px',
        backgroundColor: '#003050',
        display: 'flex',
        flexDirection: 'column',
        padding: '1.5rem 0',
        position: 'fixed',
        height: '100vh',
      }}>
        <div style={{ padding: '0 1.5rem', marginBottom: '2rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
    <div style={{
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '4px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '36px',
    height: '36px',
    }}>
    <img src={logo} alt="Guardiao EPI" style={{ height: '34px' }} />
    </div>
    <span style={{ color: 'white', fontWeight: '700', fontSize: '0.9rem', letterSpacing: '0.05em' }}>
    Guardiao EPI
    </span>
</div>
        <nav style={{ flex: 1 }}>
          {menuItems.map((item) => {
            const Icon = item.icon
            const ativo = location.pathname === item.path
            return (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                style={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '0.75rem 1.5rem',
                  backgroundColor: ativo ? 'rgba(255,255,255,0.1)' : 'transparent',
                  border: 'none',
                  borderLeft: ativo ? '3px solid #60A5FA' : '3px solid transparent',
                  color: ativo ? 'white' : 'rgba(255,255,255,0.6)',
                  cursor: 'pointer',
                  fontSize: '0.9rem',
                  textAlign: 'left',
                }}
              >
                <Icon size={18} />
                {item.label}
              </button>
            )
          })}
        </nav>

        <div style={{ padding: '0 1.5rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '1rem' }}>
          <div style={{ marginBottom: '1rem' }}>
            <div style={{
              width: '32px',
              height: '32px',
              borderRadius: '50%',
              backgroundColor: '#60A5FA',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontWeight: '700',
              fontSize: '0.85rem',
              marginBottom: '0.5rem'
            }}>
              {usuario?.username?.[0]?.toUpperCase()}
            </div>
            <p style={{ color: 'white', fontSize: '0.85rem', fontWeight: '600', margin: 0 }}>
              {usuario?.username}
            </p>
            <p style={{ color: 'rgba(255,255,255,0.5)', fontSize: '0.75rem', margin: 0, textTransform: 'capitalize' }}>
              {usuario?.perfil}
            </p>
          </div>
          <button
            onClick={handleLogout}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'none',
              border: 'none',
              color: '#EF4444',
              cursor: 'pointer',
              fontSize: '0.85rem',
              padding: 0
            }}
          >
            <LogOut size={16} />
            Sair
          </button>
        </div>
      </aside>

      <main style={{ marginLeft: '220px', flex: 1, padding: '2rem' }}>
        {children}
      </main>
    </div>
  )
}