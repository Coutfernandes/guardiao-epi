// eslint-disable-next-line*/
/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useState } from 'react'
import api from '../services/api'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(() => {
    const usuarioSalvo = localStorage.getItem('usuario')
    return usuarioSalvo ? JSON.parse(usuarioSalvo) : null
  })

  const login = async (username, password) => {
    const response = await api.post('/auth/login/', { username, password })
    const { access, refresh, usuario } = response.data
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
    localStorage.setItem('usuario', JSON.stringify(usuario))
    setUsuario(usuario)
    return usuario
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('usuario')
    setUsuario(null)
  }

  return (
    <AuthContext.Provider value={{ usuario, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}