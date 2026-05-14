import { useState, useEffect, useCallback } from 'react'
import { AlertTriangle, Camera, CheckCircle, Activity } from 'lucide-react'
import api from '../services/api'

function StatCard({ titulo, valor, subtexto, icone: Icone }) {
  return (
    <div style={{
      backgroundColor: 'white', borderRadius: '12px', padding: '1.25rem',
      border: '1px solid #E2E8F0', display: 'flex', flexDirection: 'column', gap: '0.5rem'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ backgroundColor: '#F8FAFC', padding: '0.5rem', borderRadius: '8px' }}>
          <Icone size={18} color="#64748B" />
        </div>
        <span style={{ fontSize: '0.65rem', fontWeight: '700', color: '#94A3B8', textTransform: 'uppercase' }}>{titulo}</span>
      </div>
      <div>
        <h3 style={{ fontSize: '1.75rem', fontWeight: '700', color: '#003050', margin: 0 }}>{valor}</h3>
        <p style={{ fontSize: '0.75rem', color: '#64748B', margin: 0 }}>{subtexto}</p>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [cameras, setCameras] = useState([])
  const [alertas, setAlertas] = useState([])
  const [ocorrencias, setOcorrencias] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [token] = useState(localStorage.getItem('access_token'))

  const carregarDados = useCallback(async () => {
    try {
      const [resCams, resAlts, resOcors] = await Promise.all([
        api.get('/cameras/'),
        api.get('/deteccao/alertas/'),
        api.get('/deteccao/ocorrencias/')
      ])
      setCameras(resCams.data)
      setAlertas(resAlts.data)
      setOcorrencias(resOcors.data)
    } catch (err) {
      console.error('Erro de conexao:', err)
    } finally {
      setCarregando(false)
    }
  }, [])

  useEffect(() => {
    const inicializar = async () => { await carregarDados() }
    inicializar()
    const intervalo = setInterval(carregarDados, 30000)
    return () => clearInterval(intervalo)
  }, [carregarDados])

  const camerasOnline = cameras.filter(c => c.status === 'online').length
  const alertasPendentes = alertas.filter(a => !a.reconhecido).length
  const ocorrenciasHoje = ocorrencias.filter(o =>
    new Date(o.criado_em).toDateString() === new Date().toDateString()
  )
  const conformesHoje = ocorrenciasHoje.filter(o => o.status === 'conforme').length
  const naoConformesHoje = ocorrenciasHoje.filter(o => o.tipo === 'epi_ausente').length
  const taxaHoje = ocorrenciasHoje.length > 0
    ? Math.round((conformesHoje / ocorrenciasHoje.length) * 100) : 0

  const traduzirMensagem = (msg) => {
    if (!msg) return ''
    return msg.replace(/no helmet|no gloves|no goggles|no vest|no shoes/g, m => ({
      'no helmet': 'sem capacete', 'no gloves': 'sem luvas',
      'no goggles': 'sem oculos', 'no vest': 'sem colete', 'no shoes': 'sem botina'
    }[m]))
  }

  const temEpiAusente = (camera) =>
    ocorrenciasHoje.some(o => o.camera === camera.id && o.tipo === 'epi_ausente')

  const alertasOrdenados = [
    ...alertas.filter(a => !a.reconhecido && a.nivel === 'critico').slice(0, 3),
    ...alertas.filter(a => !a.reconhecido && a.nivel === 'aviso').slice(0, 3),
  ]

  if (carregando) return <div style={{ padding: '2rem', color: '#64748B' }}>Carregando Dashboard...</div>

  return (
    <div style={{ padding: '2rem', backgroundColor: '#F8FAFC', minHeight: '100vh' }}>
      <header style={{ marginBottom: '2rem' }}>
        <h1 style={{ fontSize: '1.8rem', fontWeight: '800', color: '#003050', margin: 0 }}>Dashboard</h1>
        <p style={{ color: '#64748B', margin: 0 }}>Monitoramento de EPIs em tempo real</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <StatCard titulo="Cameras" valor={cameras.length} subtexto={`${camerasOnline} online`} icone={Camera} />
        <StatCard titulo="Online" valor={camerasOnline} subtexto={`de ${cameras.length}`} icone={Activity} />
        <StatCard titulo="Alertas" valor={alertasPendentes} subtexto="ativos agora" icone={AlertTriangle} />
        <StatCard titulo="Conformidade" valor={`${taxaHoje}%`} subtexto="media hoje" icone={CheckCircle} />
        <StatCard titulo="Ocorrencias" valor={ocorrenciasHoje.length} subtexto="total hoje" icone={Activity} />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ backgroundColor: 'white', border: '1px solid #E2E8F0', borderRadius: '12px', padding: '1.25rem' }}>
          <p style={{ color: '#64748B', fontSize: '0.8rem', margin: '0 0 0.5rem 0' }}>Conformes Hoje</p>
          <p style={{ color: '#22C55E', fontSize: '2rem', fontWeight: '700', margin: 0 }}>{conformesHoje}</p>
        </div>
        <div style={{ backgroundColor: 'white', border: '1px solid #E2E8F0', borderRadius: '12px', padding: '1.25rem' }}>
          <p style={{ color: '#64748B', fontSize: '0.8rem', margin: '0 0 0.5rem 0' }}>Nao Conformes Hoje</p>
          <p style={{ color: '#EF4444', fontSize: '2rem', fontWeight: '700', margin: 0 }}>{naoConformesHoje}</p>
        </div>
        <div style={{ backgroundColor: 'white', border: '1px solid #E2E8F0', borderRadius: '12px', padding: '1.25rem' }}>
          <p style={{ color: '#64748B', fontSize: '0.8rem', margin: '0 0 0.5rem 0' }}>Taxa de Conformidade</p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '0.5rem' }}>
            <div style={{ flex: 1, height: '8px', backgroundColor: '#F1F5F9', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{
                width: `${taxaHoje}%`, height: '100%',
                backgroundColor: taxaHoje >= 70 ? '#22C55E' : taxaHoje >= 40 ? '#F59E0B' : '#EF4444',
                borderRadius: '4px'
              }} />
            </div>
            <span style={{ color: '#003050', fontWeight: '700' }}>{taxaHoje}%</span>
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.6fr 1fr', gap: '1.5rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', alignItems: 'start' }}>
          {cameras.slice(0, 4).map(cam => {
            const alerta = temEpiAusente(cam)
            return (
              <div key={cam.id} style={{
                backgroundColor: 'white', borderRadius: '12px', padding: '1rem',
                border: '1px solid #E2E8F0'
              }}>
                <div style={{
                  height: '220px', borderRadius: '8px', overflow: 'hidden',
                  marginBottom: '0.75rem', position: 'relative', backgroundColor: '#000'
                }}>
                  {cam.status === 'online' && token ? (
                    <img
                      src={`http://127.0.0.1:8000/api/cameras/${cam.id}/stream/?token=${token}`}
                      alt={cam.nome}
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                  ) : (
                    <div style={{
                      width: '100%', height: '100%', backgroundColor: '#F1F5F9',
                      display: 'flex', alignItems: 'center', justifyContent: 'center'
                    }}>
                      <Camera size={32} color="#CBD5E0" />
                    </div>
                  )}
                  {alerta && (
                    <div style={{
                      position: 'absolute', top: 0, left: 0, right: 0,
                      backgroundColor: '#EF444490', padding: '0.3rem 0.5rem',
                      display: 'flex', alignItems: 'center', gap: '0.3rem'
                    }}>
                      <AlertTriangle size={12} color="white" />
                      <span style={{ color: 'white', fontSize: '0.65rem', fontWeight: '700' }}>EPI AUSENTE</span>
                    </div>
                  )}
                  <div style={{ position: 'absolute', top: '8px', right: '8px', display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <div style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: cam.status === 'online' ? '#22C55E' : '#EF4444' }} />
                    <span style={{ fontSize: '0.55rem', fontWeight: 'bold', color: 'white', textShadow: '0 1px 2px rgba(0,0,0,0.8)' }}>{cam.identificador}</span>
                  </div>
                </div>
                <h5 style={{ margin: 0, color: '#003050', fontSize: '0.9rem' }}>{cam.nome}</h5>
                <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.75rem', color: '#64748B' }}>
                  {alerta ? 'EPI Ausente Detectado' : `Status: ${cam.status}`}
                </p>
              </div>
            )
          })}
        </div>

        <div style={{ backgroundColor: 'white', padding: '1.5rem', borderRadius: '16px', border: '1px solid #E2E8F0' }}>
          <h4 style={{ margin: '0 0 1.25rem 0', color: '#003050', fontSize: '1rem' }}>Alertas Recentes</h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {alertasOrdenados.length === 0 ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#22C55E' }}>
                <CheckCircle size={16} />
                <span style={{ fontSize: '0.85rem' }}>Nenhum alerta pendente</span>
              </div>
            ) : (
              alertasOrdenados.map(alerta => (
                <div key={alerta.id} style={{
                  display: 'flex', alignItems: 'flex-start', gap: '0.75rem',
                  paddingBottom: '0.75rem', borderBottom: '1px solid #F1F5F9'
                }}>
                  <AlertTriangle size={16} color={alerta.nivel === 'critico' ? '#EF4444' : '#F59E0B'} style={{ marginTop: '3px' }} />
                  <div style={{ flex: 1 }}>
                    <p style={{ fontSize: '0.85rem', color: '#003050', margin: 0, fontWeight: '500', lineHeight: '1.2' }}>
                      {traduzirMensagem(alerta.mensagem)}
                    </p>
                    <p style={{ fontSize: '0.7rem', color: '#94A3B8', margin: '0.25rem 0 0 0' }}>
                      {new Date(alerta.criado_em).toLocaleTimeString()} • {alerta.camera_nome}
                    </p>
                  </div>
                  <div style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: alerta.nivel === 'critico' ? '#EF4444' : '#F59E0B', marginTop: '6px' }} />
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}