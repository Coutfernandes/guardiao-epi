import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import logo from '../assets/logo.png'

export default function Login() {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [mostrarSenha, setMostrarSenha] = useState(false)
  const [lembrar, setLembrar] = useState(true)
  const [erro, setErro] = useState('')
  const [carregando, setCarregando] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setErro('')
    setCarregando(true)
    try {
      await login(username, password)
      navigate('/')
    } catch {
      setErro('Usuario ou senha invalidos')
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#F8FAFC',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <img src={logo} alt="Guardiao EPI" style={{ height: '70px', marginBottom: '0.75rem' }} />
        <h1 style={{ color: '#003050', fontSize: '1.4rem', fontWeight: '700', letterSpacing: '0.15em', margin: 0 }}>
          GUARDIAO EPI
        </h1>
        <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginTop: '0.3rem' }}>
          Transformando Cameras em Seguranca Ativa
        </p>
      </div>

      <div style={{
        backgroundColor: 'white',
        borderRadius: '12px',
        padding: '2rem',
        width: '100%',
        maxWidth: '420px',
        boxShadow: '0 1px 6px rgba(0,0,0,0.06)',
        border: '1px solid #E2E8F0',
      }}>
        <h2 style={{ color: '#003050', fontSize: '1.2rem', fontWeight: '700', marginBottom: '0.25rem',textAlign: 'center' }}>
          Bem-vindo de volta
        </h2>
        <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '1.75rem', textAlign: 'center' }}>
          Faca login para continuar
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{
              display: 'block',
              color: '#64748B',
              fontSize: '0.72rem',
              fontWeight: '600',
              marginBottom: '0.5rem',
              letterSpacing: '0.08em'
            }}>
              USUARIO
            </label>
            <div style={{ position: 'relative' }}>
              <span style={{
                position: 'absolute',
                left: '0.85rem',
                top: '50%',
                transform: 'translateY(-50%)',
                color: '#94A3B8',
                fontSize: '1rem'
              }}>
              </span>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="nome de usuario"
                required
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem 0.75rem 2.25rem',
                  border: '1px solid #E2E8F0',
                  borderRadius: '8px',
                  fontSize: '0.9rem',
                  outline: 'none',
                  color: '#003050',
                  backgroundColor: 'white'
                }}
              />
            </div>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{
              display: 'block',
              color: '#64748B',
              fontSize: '0.72rem',
              fontWeight: '600',
              marginBottom: '0.5rem',
              letterSpacing: '0.08em'
            }}>
              SENHA
            </label>
            <div style={{ position: 'relative' }}>
              <span style={{
                position: 'absolute',
                left: '0.85rem',
                top: '50%',
                transform: 'translateY(-50%)',
                color: '#94A3B8',
                fontSize: '0.9rem'
              }}>
              </span>
              <input
                type={mostrarSenha ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                style={{
                  width: '100%',
                  padding: '0.75rem 3rem 0.75rem 2.25rem',
                  border: '1px solid #E2E8F0',
                  borderRadius: '8px',
                  fontSize: '0.9rem',
                  outline: 'none',
                  color: '#003050',
                  backgroundColor: 'white'
                }}
              />
              <button
                type="button"
                onClick={() => setMostrarSenha(!mostrarSenha)}
                style={{
                  position: 'absolute',
                  right: '0.85rem',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: '#94A3B8',
                  fontSize: '0.85rem'
                }}
              >
                {mostrarSenha ? 'ocultar' : '👁'}
              </button>
            </div>
          </div>

          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '1.5rem'
          }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer', fontSize: '0.85rem', color: '#64748B' }}>
              <input
                type="checkbox"
                checked={lembrar}
                onChange={(e) => setLembrar(e.target.checked)}
                style={{ accentColor: '#003050' }}
              />
              Lembrar acesso
            </label>
            <span style={{ fontSize: '0.85rem', color: '#003050', fontWeight: '600', cursor: 'pointer' }}>
              Esquecer
            </span>
          </div>

          {erro && (
            <p style={{ color: '#DC2626', fontSize: '0.85rem', marginBottom: '1rem', textAlign: 'center' }}>
              {erro}
            </p>
          )}

          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '1rem',
            marginBottom: '1rem'
          }}>
            <div style={{ flex: 1, height: '1px', backgroundColor: '#E2E8F0' }} />
            <span style={{ color: '#94A3B8', fontSize: '0.8rem' }}>ou entre com</span>
            <div style={{ flex: 1, height: '1px', backgroundColor: '#E2E8F0' }} />
          </div>

          <button
            type="submit"
            disabled={carregando}
            style={{
              width: '100%',
              padding: '0.875rem',
              backgroundColor: carregando ? '#64748B' : '#003050',
              color: 'white',
              border: 'none',
              borderRadius: '50px',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: carregando ? 'not-allowed' : 'pointer',
            }}
          >
            {carregando ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
      </div>

      <p style={{ marginTop: '1.5rem', fontSize: '0.85rem', color: '#64748B' }}>
        Nao tem uma conta?{' '}
        <span style={{ color: '#003050', fontWeight: '600', cursor: 'pointer' }}>
          Cadastre-se
        </span>
      </p>
    </div>
  )
}