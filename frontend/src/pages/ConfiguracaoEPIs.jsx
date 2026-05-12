import { useState, useEffect, useCallback } from 'react'
import api from '../services/api'

// Removi o eslint-disable para provar que o código está limpo!

const EPIS_DISPONIVEIS = [
  { tipo: 'helmet', nome: 'Capacete', descricao: 'Capacete de segurança' },
  { tipo: 'gloves', nome: 'Luvas', descricao: 'Luvas de proteção' },
  { tipo: 'goggles', nome: 'Óculos', descricao: 'Óculos de proteção' },
  { tipo: 'vest', nome: 'Colete', descricao: 'Colete refletivo' },
  { tipo: 'shoes', nome: 'Botina', descricao: 'Botina de segurança' },
  { tipo: 'mask', nome: 'Máscara', descricao: 'Máscara de proteção' },
]

export default function ConfiguracaoEPIs() {
  const [cameras, setCameras] = useState([])
  const [cameraSelecionada, setCameraSelecionada] = useState(null)
  const [configuracoes, setConfiguracoes] = useState([])
  const [loading, setLoading] = useState(true) // Boa prática de QA: Feedback de carregamento

  // Usamos useCallback para que a função seja estável e não cause re-renders infinitos
  const carregarConfiguracoes = useCallback(async (cameraId) => {
    try {
      const res = await api.get(`/cameras/${cameraId}/epis/`)
      setConfiguracoes(res.data)
    } catch (err) {
      console.error("Erro ao buscar configurações:", err)
    }
  }, [])

  useEffect(() => {
    const inicializarDados = async () => {
      setLoading(true)
      try {
        const res = await api.get('/cameras/')
        setCameras(res.data)
        
        if (res.data.length > 0) {
          const primeira = res.data[0]
          setCameraSelecionada(primeira)
          // Chamamos a segunda API direto aqui para evitar a "cascata" de useEffects
          await carregarConfiguracoes(primeira.id)
        }
      } catch (err) {
        console.error("Erro na inicialização:", err)
      } finally {
        setLoading(false)
      }
    }

    inicializarDados()
  }, [carregarConfiguracoes]) // Dependência limpa

  const handleToggle = async (tipo) => {
    if (!cameraSelecionada) return
    
    const atual = configuracoes.find(c => c.tipo_epi === tipo)
    const novoStatus = atual ? !atual.ativo : true

    try {
      await api.post(`/cameras/${cameraSelecionada.id}/epis/`, {
        tipo_epi: tipo,
        ativo: novoStatus
      })
      // Atualiza apenas as configurações da câmera atual
      await carregarConfiguracoes(cameraSelecionada.id)
    } catch (err) {
      console.error("Erro ao salvar EPI:", err)
    }
  }

  // Helper para facilitar a leitura no render
  const epiAtivo = (tipo) => configuracoes.find(c => c.tipo_epi === tipo)?.ativo || false
  const ativos = configuracoes.filter(c => c.ativo).length

  if (loading) return <div style={{ padding: '2rem', color: '#64748B' }}>Carregando configurações...</div>

  return (
    <div style={{ padding: '2rem', backgroundColor: '#F8FAFC', minHeight: '100vh' }}>
      <div style={{ marginBottom: '2rem' }}>
        <h1 style={{ color: '#003050', fontSize: '1.5rem', fontWeight: '700', margin: 0 }}>
          Configuração de EPIs
        </h1>
        <p style={{ color: '#64748B', fontSize: '0.9rem', marginTop: '0.25rem' }}>
          {cameraSelecionada ? `Monitorando ${cameraSelecionada.nome}` : 'Selecione uma câmera'} — {ativos} ativos
        </p>
      </div>

      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ color: '#64748B', fontSize: '0.75rem', fontWeight: '700', letterSpacing: '0.05em' }}>
          CÂMERA ATIVA
        </label>
        <select
          value={cameraSelecionada?.id || ''}
          onChange={(e) => {
            const cam = cameras.find(c => c.id === parseInt(e.target.value))
            setCameraSelecionada(cam)
            carregarConfiguracoes(cam.id) // Busca as novas configs imediatamente na troca
          }}
          style={{
            display: 'block', marginTop: '0.5rem', padding: '0.6rem',
            borderRadius: '8px', border: '1px solid #E2E8F0', width: '300px'
          }}
        >
          {cameras.map(c => (
            <option key={c.id} value={c.id}>{c.nome}</option>
          ))}
        </select>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
        {EPIS_DISPONIVEIS.map(epi => (
          <div key={epi.tipo} style={{
            backgroundColor: 'white', borderRadius: '12px', padding: '1.25rem',
            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
          }}>
            <div>
              <p style={{ color: '#003050', fontWeight: '600', margin: 0 }}>{epi.nome}</p>
              <p style={{ color: '#94A3B8', fontSize: '0.75rem', margin: 0 }}>{epi.descricao}</p>
            </div>
            <div
              onClick={() => handleToggle(epi.tipo)}
              style={{
                width: '40px', height: '20px', borderRadius: '10px',
                backgroundColor: epiAtivo(epi.tipo) ? '#003050' : '#E2E8F0',
                cursor: 'pointer', position: 'relative', transition: '0.2s'
              }}
            >
              <div style={{
                width: '14px', height: '14px', borderRadius: '50%', backgroundColor: 'white',
                position: 'absolute', top: '3px', left: epiAtivo(epi.tipo) ? '23px' : '3px',
                transition: '0.2s'
              }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}