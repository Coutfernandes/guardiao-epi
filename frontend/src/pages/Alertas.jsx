/* eslint-disable react-hooks/set-state-in-effect */
import { useState, useEffect } from 'react'
import { AlertTriangle } from 'lucide-react'
import api from '../services/api'

const TRADUCAO_EPI = {
  'no helmet': 'sem capacete',
  'no gloves': 'sem luvas',
  'no goggles': 'sem oculos',
  'no vest': 'sem colete',
  'no shoes': 'sem botina',
  'helmet': 'capacete',
  'gloves': 'luvas',
  'goggles': 'oculos',
  'vest': 'colete',
  'shoes': 'botina',
}

const traduzirEpi = (epi) => TRADUCAO_EPI[epi] || epi

function NivelBadge({ nivel }) {
  const config = {
    critico: { cor: '#EF4444', fundo: '#FEE2E2', texto: 'CRITICO' },
    aviso: { cor: '#F59E0B', fundo: '#FEF3C7', texto: 'AVISO' },
    info: { cor: '#3B82F6', fundo: '#DBEAFE', texto: 'INFO' },
  }
  const { cor, fundo, texto } = config[nivel] || config.aviso
  return (
    <span style={{
      backgroundColor: fundo, color: cor,
      fontSize: '0.7rem', fontWeight: '700',
      padding: '0.2rem 0.5rem', borderRadius: '4px',
      letterSpacing: '0.05em'
    }}>
      {texto}
    </span>
  )
}

export default function Alertas() {
  const [alertas, setAlertas] = useState([])
  const [filtro, setFiltro] = useState('todos')

  const carregarAlertas = async () => {
    const res = await api.get('/deteccao/alertas/')
    setAlertas(res.data)
  }

  useEffect(() => {
    carregarAlertas()
    const intervalo = setInterval(carregarAlertas, 30000)
    return () => clearInterval(intervalo)
  }, [])

  const handleReconhecer = async (id) => {
    await api.patch(`/deteccao/alertas/${id}/reconhecer/`)
    await carregarAlertas()
  }

  const handleReconhecerTodos = async () => {
    const pendentes = alertas.filter(a => !a.reconhecido)
    await Promise.all(pendentes.map(a => api.patch(`/deteccao/alertas/${a.id}/reconhecer/`)))
    await carregarAlertas()
}

  const alertasFiltrados = alertas.filter(a => {
    if (filtro === 'todos') return true
    if (filtro === 'criticos') return a.nivel === 'critico'
    if (filtro === 'avisos') return a.nivel === 'aviso'
    if (filtro === 'pendentes') return !a.reconhecido
    return true
  })

  const naoReconhecidos = alertas.filter(a => !a.reconhecido).length

  return (
    <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
          <div>
            <h1 style={{ color: '#003050', fontSize: '1.5rem', fontWeight: '700', margin: 0 }}>
            Alertas </h1>
            <p style={{ color: '#64748B', fontSize: '0.9rem', marginTop: '0.25rem' }}>
              {naoReconhecidos} alertas nao reconhecidos
            </p>
        </div>
        {naoReconhecidos > 0 && (
        <button
          onClick={handleReconhecerTodos}
          style={{
          padding: '0.65rem 1.25rem',
          backgroundColor: '#003050',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          fontSize: '0.85rem',
          fontWeight: '600',
        }}
    >
        Reconhecer Todos
      </button>
        )}
      </div>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        {['todos', 'criticos', 'avisos', 'pendentes'].map(f => (
          <button
            key={f}
            onClick={() => setFiltro(f)}
            style={{
              padding: '0.4rem 1rem',
              borderRadius: '6px',
              border: filtro === f ? 'none' : '1px solid #E2E8F0',
              backgroundColor: filtro === f ? '#003050' : 'white',
              color: filtro === f ? 'white' : '#64748B',
              cursor: 'pointer',
              fontSize: '0.85rem',
              fontWeight: filtro === f ? '600' : '400',
              textTransform: 'capitalize'
            }}
          >
            {f === 'todos' ? 'Todos' : f === 'criticos' ? 'Criticos' : f === 'avisos' ? 'Alerta' : 'Info'}
          </button>
        ))}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {alertasFiltrados.map(alerta => (
          <div key={alerta.id} style={{
            backgroundColor: alerta.reconhecido ? '#F8FAFC' : 'white',
            border: '1px solid #E2E8F0',
            borderRadius: '8px',
            padding: '1rem 1.25rem',
            display: 'flex',
            alignItems: 'center',
            gap: '1rem'
          }}>
            <AlertTriangle
              size={20}
              color={alerta.nivel === 'critico' ? '#EF4444' : '#F59E0B'}
            />
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.25rem' }}>
                <NivelBadge nivel={alerta.nivel} />
                <span style={{ color: '#94A3B8', fontSize: '0.8rem' }}>
                  {new Date(alerta.criado_em).toLocaleString('pt-BR')}
                </span>
              </div>
              <p style={{ color: '#003050', fontSize: '0.9rem', margin: 0, fontWeight: '500' }}>
                {alerta.mensagem.replace(/no helmet|no gloves|no goggles|no vest|no shoes|helmet|gloves|goggles|vest|shoes/g, match => traduzirEpi(match))}
              </p>
              <p style={{ color: '#94A3B8', fontSize: '0.8rem', margin: '0.25rem 0 0 0' }}>
                {alerta.camera_nome}
              </p>
            </div>
            {!alerta.reconhecido ? (
              <button
                onClick={() => handleReconhecer(alerta.id)}
                style={{
                  padding: '0.4rem 0.85rem',
                  border: '1px solid #E2E8F0',
                  borderRadius: '6px',
                  background: 'white',
                  color: '#003050',
                  cursor: 'pointer',
                  fontSize: '0.8rem',
                  fontWeight: '600',
                  whiteSpace: 'nowrap'
                }}
              >
                Reconhecer
              </button>
            ) : (
              <span style={{ color: '#22C55E', fontSize: '0.8rem', fontWeight: '600', whiteSpace: 'nowrap' }}>
                Reconhecido
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}