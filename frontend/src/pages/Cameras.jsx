import { useState, useEffect } from 'react'
import { Camera, Plus, Pencil, Trash2, Search, Wifi } from 'lucide-react'
import api from '../services/api'

function StatusBadge({ status }) {
  const config = {
    online: { cor: '#22C55E', texto: 'Online' },
    offline: { cor: '#EF4444', texto: 'Offline' },
    alerta: { cor: '#F59E0B', texto: 'Alerta' },
  }
  const { cor, texto } = config[status] || config.offline
  return (
    <span style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', fontSize: '0.8rem', color: cor, fontWeight: '600' }}>
      <span style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: cor, display: 'inline-block' }} />
      {texto}
    </span>
  )
}

function ModalCamera({ camera, onFechar, onSalvar }) {
  const [form, setForm] = useState(camera || {
    nome: '', identificador: '', url_stream: '', setor: '', localizacao: ''
  })

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    await onSalvar(form)
  }

  const inputStyle = {
    width: '100%', padding: '0.65rem 0.85rem', border: '1px solid #E2E8F0',
    borderRadius: '8px', fontSize: '0.9rem', color: '#003050',
    backgroundColor: 'white', boxSizing: 'border-box', outline: 'none'
  }
  const labelStyle = {
    display: 'block', fontSize: '0.72rem', fontWeight: '600',
    color: '#64748B', marginBottom: '0.4rem', letterSpacing: '0.06em'
  }

  return (
    <div style={{
      position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.4)',
      display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000
    }}>
      <div style={{ backgroundColor: 'white', borderRadius: '12px', padding: '2rem', width: '100%', maxWidth: '480px' }}>
        <h2 style={{ color: '#003050', marginBottom: '1.5rem', fontSize: '1.1rem' }}>
          {camera ? 'Editar Camera' : 'Adicionar Camera'}
        </h2>
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
            <div>
              <label style={labelStyle}>NOME</label>
              <input name="nome" value={form.nome} onChange={handleChange} required style={inputStyle} placeholder="Entrada Principal" />
            </div>
            <div>
              <label style={labelStyle}>IDENTIFICADOR</label>
              <input name="identificador" value={form.identificador} onChange={handleChange} required style={inputStyle} placeholder="CAM-01" />
            </div>
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label style={labelStyle}>URL STREAM (RTSP)</label>
            <input name="url_stream" value={form.url_stream} onChange={handleChange} required style={inputStyle} placeholder="rtsp://192.168.1.100/stream" />
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
            <div>
              <label style={labelStyle}>SETOR</label>
              <input name="setor" value={form.setor} onChange={handleChange} required style={inputStyle} placeholder="Producao" />
            </div>
            <div>
              <label style={labelStyle}>LOCALIZACAO</label>
              <input name="localizacao" value={form.localizacao} onChange={handleChange} style={inputStyle} placeholder="Portaria A" />
            </div>
          </div>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
            <button type="button" onClick={onFechar} style={{
              padding: '0.65rem 1.25rem', border: '1px solid #E2E8F0',
              borderRadius: '8px', background: 'white', color: '#64748B', cursor: 'pointer'
            }}>
              Cancelar
            </button>
            <button type="submit" style={{
              padding: '0.65rem 1.25rem', border: 'none',
              borderRadius: '8px', backgroundColor: '#003050', color: 'white',
              fontWeight: '600', cursor: 'pointer'
            }}>
              Salvar
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default function Cameras() {
  const [cameras, setCameras] = useState([])
  const [busca, setBusca] = useState('')
  const [modal, setModal] = useState(null)

  const carregarCameras = async () => {
    const res = await api.get('/cameras/')
    setCameras(res.data)
  }


useEffect(() => {
  // eslint-disable-next-line react-hooks/set-state-in-effect
  void carregarCameras()
}, [])

  const handleSalvar = async (form) => {
    if (form.id) {
      await api.put(`/cameras/${form.id}/`, form)
    } else {
      await api.post('/cameras/', form)
    }
    await carregarCameras()
    setModal(null)
  }
  const handleVerificar = async (id) => {
      await api.post(`/cameras/${id}/verificar/`)
      await carregarCameras()
}
  const handleDeletar = async (id) => {
    if (window.confirm('Deseja remover esta camera?')) {
      await api.delete(`/cameras/${id}/`)
      await carregarCameras()
    }
  }

  const camerasFiltradas = cameras.filter(c =>
    c.nome.toLowerCase().includes(busca.toLowerCase()) ||
    c.identificador.toLowerCase().includes(busca.toLowerCase()) ||
    c.setor.toLowerCase().includes(busca.toLowerCase())
  )

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ color: '#003050', fontSize: '1.5rem', fontWeight: '700', margin: 0 }}>Cameras</h1>
          <p style={{ color: '#64748B', fontSize: '0.9rem', marginTop: '0.25rem' }}>Gerencie suas cameras de monitoramento</p>
        </div>
        <button onClick={() => setModal({})} style={{
          display: 'flex', alignItems: 'center', gap: '0.5rem',
          backgroundColor: '#003050', color: 'white', border: 'none',
          borderRadius: '8px', padding: '0.65rem 1.25rem', cursor: 'pointer', fontWeight: '600'
        }}>
          <Plus size={16} /> Adicionar
        </button>
      </div>

      <div style={{ position: 'relative', marginBottom: '1.5rem', maxWidth: '320px' }}>
        <Search size={16} style={{ position: 'absolute', left: '0.85rem', top: '50%', transform: 'translateY(-50%)', color: '#94A3B8' }} />
        <input
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
          placeholder="Buscar cameras..."
          style={{
            width: '100%', padding: '0.65rem 1rem 0.65rem 2.5rem',
            border: '1px solid #E2E8F0', borderRadius: '8px',
            fontSize: '0.9rem', outline: 'none', boxSizing: 'border-box'
          }}
        />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '1.25rem' }}>
        {camerasFiltradas.map(camera => (
          <div key={camera.id} style={{
            backgroundColor: 'white', borderRadius: '12px',
            border: '1px solid #E2E8F0', overflow: 'hidden'
          }}>
            <div style={{
              backgroundColor: '#F1F5F9', height: '180px',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              position: 'relative', overflow: 'hidden'
        }}>
            <span style={{
              position: 'absolute', top: '0.75rem', left: '0.75rem',
              backgroundColor: 'rgba(0,0,0,0.5)', color: 'white',
              fontSize: '0.75rem', fontWeight: '700', padding: '0.2rem 0.5rem',
              borderRadius: '4px', zIndex: 1
            }}>
              {camera.identificador}
            </span>
          {camera.status === 'online' ? (
              <img
              src={`http://127.0.0.1:8000/api/cameras/${camera.id}/stream/?token=${localStorage.getItem('access_token')}`}
              alt={camera.nome}
              style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          />
        ) : (
          <Camera size={40} color="#CBD5E1" />
        )}
      </div>
            <div style={{ padding: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                <h3 style={{ color: '#003050', fontSize: '0.95rem', fontWeight: '600', margin: 0 }}>{camera.nome}</h3>
                <StatusBadge status={camera.status} />
              </div>
              <p style={{ color: '#94A3B8', fontSize: '0.8rem', margin: '0 0 1rem 0' }}>
                {camera.setor} {camera.localizacao ? `• ${camera.localizacao}` : ''}
              </p>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <button onClick={() => setModal(camera)} style={{
                  flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center',
                  gap: '0.4rem', padding: '0.5rem', border: '1px solid #E2E8F0',
                  borderRadius: '8px', background: 'white', color: '#003050',
                  cursor: 'pointer', fontSize: '0.85rem'
                }}>
                  <Pencil size={14} /> Editar
                </button>
                <button onClick={() => handleVerificar(camera.id)} style={{
                  padding: '0.5rem 0.75rem', border: '1px solid #DBEAFE',
                  borderRadius: '8px', background: 'white', color: '#3B82F6',
                  cursor: 'pointer'
                }}>
                  <Wifi size={14} />
                </button>
                <button onClick={() => handleDeletar(camera.id)} style={{
                  padding: '0.5rem 0.75rem', border: '1px solid #FEE2E2',
                  borderRadius: '8px', background: 'white', color: '#EF4444',
                  cursor: 'pointer'
                }}>
                  <Trash2 size={14} />
                </button>
              </div>

            </div>
          </div>
        ))}
      </div>

      {modal !== null && (
        <ModalCamera
          camera={Object.keys(modal).length > 0 ? modal : null}
          onFechar={() => setModal(null)}
          onSalvar={handleSalvar}
        />
      )}
    </div>
  )
}