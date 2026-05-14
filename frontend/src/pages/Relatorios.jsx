import { useState, useEffect } from 'react'
import api from '../services/api'

const TRADUCAO_EPI = {
  'no helmet': 'sem capacete',
  'no gloves': 'sem luvas',
  'no goggles': 'sem oculos',
  'no vest': 'sem colete',
  'no shoes': 'sem botina',
}

const traduzirEpi = (epi) => TRADUCAO_EPI[epi] || epi

function StatusBadge({ status }) {
  const config = {
    conforme: { cor: '#22C55E', fundo: '#DCFCE7', texto: 'Conforme' },
    nao_conforme: { cor: '#EF4444', fundo: '#FEE2E2', texto: 'Nao Conforme' },
  }
  const { cor, fundo, texto } = config[status] || config.nao_conforme
  return (
    <span style={{
      backgroundColor: fundo, color: cor,
      fontSize: '0.75rem', fontWeight: '600',
      padding: '0.2rem 0.6rem', borderRadius: '4px'
    }}>
      {texto}
    </span>
  )
}

export default function Relatorios() {
  const [ocorrencias, setOcorrencias] = useState([])
  const [cameras, setCameras] = useState([])
  const [filtros, setFiltros] = useState({ camera: '', tipo: '', status: '' })
  const [carregando, setCarregando] = useState(true)

  const handleDownloadPDF = async () => {
    const res = await api.get('/deteccao/relatorio/pdf/', { responseType: 'blob' })
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', 'relatorio_guardiao_epi.pdf')
    document.body.appendChild(link)
    link.click()
    link.remove()
  }

  useEffect(() => {
    const carregar = async () => {
      setCarregando(true)
      const [resOcorrencias, resCameras] = await Promise.all([
        api.get('/deteccao/ocorrencias/'),
        api.get('/cameras/')
      ])
      setOcorrencias(resOcorrencias.data)
      setCameras(resCameras.data)
      setCarregando(false)
    }
    carregar()
  }, [])

  const ocorrenciasFiltradas = ocorrencias.filter(o => {
    if (filtros.camera && o.camera !== parseInt(filtros.camera)) return false
    if (filtros.tipo && o.tipo !== filtros.tipo) return false
    if (filtros.status && o.status !== filtros.status) return false
    return true
  })

  const totalConforme = ocorrenciasFiltradas.filter(o => o.status === 'conforme').length
  const totalNaoConforme = ocorrenciasFiltradas.filter(o => o.tipo === 'epi_ausente').length
  const taxaConformidade = ocorrenciasFiltradas.length > 0
    ? Math.round((totalConforme / ocorrenciasFiltradas.length) * 100) : 0

  const selectStyle = {
    padding: '0.6rem 1rem',
    border: '1px solid #E2E8F0',
    borderRadius: '8px',
    fontSize: '0.85rem',
    color: '#003050',
    backgroundColor: 'white',
    outline: 'none',
    cursor: 'pointer'
  }

  if (carregando) return <div style={{ padding: '2rem', color: '#64748B' }}>Carregando...</div>

  return (
    <div>
      <div style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h1 style={{ color: '#003050', fontSize: '1.5rem', fontWeight: '700', margin: 0 }}>
              Relatorios
            </h1>
            <p style={{ color: '#64748B', fontSize: '0.9rem', marginTop: '0.25rem' }}>
              Historico de ocorrencias e dados do monitoramento
            </p>
          </div>
          <button
            onClick={handleDownloadPDF}
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
            Baixar Relatorio PDF
          </button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '1rem', marginBottom: '2rem' }}>
        <div style={{ backgroundColor: 'white', border: '1px solid #E2E8F0', borderRadius: '12px', padding: '1.25rem' }}>
          <p style={{ color: '#64748B', fontSize: '0.8rem', margin: '0 0 0.5rem 0' }}>Total de Ocorrencias</p>
          <p style={{ color: '#003050', fontSize: '2rem', fontWeight: '700', margin: 0 }}>{ocorrenciasFiltradas.length}</p>
        </div>
        <div style={{ backgroundColor: 'white', border: '1px solid #E2E8F0', borderRadius: '12px', padding: '1.25rem' }}>
          <p style={{ color: '#64748B', fontSize: '0.8rem', margin: '0 0 0.5rem 0' }}>Taxa de Conformidade</p>
          <p style={{ color: '#22C55E', fontSize: '2rem', fontWeight: '700', margin: 0 }}>{taxaConformidade}%</p>
        </div>
        <div style={{ backgroundColor: 'white', border: '1px solid #E2E8F0', borderRadius: '12px', padding: '1.25rem' }}>
          <p style={{ color: '#64748B', fontSize: '0.8rem', margin: '0 0 0.5rem 0' }}>Nao Conformidades</p>
          <p style={{ color: '#EF4444', fontSize: '2rem', fontWeight: '700', margin: 0 }}>{totalNaoConforme}</p>
        </div>
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        <select
          value={filtros.camera}
          onChange={(e) => setFiltros({ ...filtros, camera: e.target.value })}
          style={selectStyle}
        >
          <option value="">Todas as cameras</option>
          {cameras.map(c => (
            <option key={c.id} value={c.id}>{c.nome}</option>
          ))}
        </select>

        <select
          value={filtros.tipo}
          onChange={(e) => setFiltros({ ...filtros, tipo: e.target.value })}
          style={selectStyle}
        >
          <option value="">Todos os tipos</option>
          <option value="epi_ausente">EPI Ausente</option>
          <option value="conformidade">Conformidade</option>
          <option value="equipment_fault">Falha de Equipamento</option>
        </select>

        <select
          value={filtros.status}
          onChange={(e) => setFiltros({ ...filtros, status: e.target.value })}
          style={selectStyle}
        >
          <option value="">Todos os status</option>
          <option value="conforme">Conforme</option>
          <option value="nao_conforme">Nao Conforme</option>
        </select>

        <button
          onClick={() => setFiltros({ camera: '', tipo: '', status: '' })}
          style={{
            padding: '0.6rem 1rem',
            border: '1px solid #E2E8F0',
            borderRadius: '8px',
            background: 'white',
            color: '#64748B',
            cursor: 'pointer',
            fontSize: '0.85rem'
          }}
        >
          Limpar filtros
        </button>
      </div>

      <div style={{ backgroundColor: 'white', border: '1px solid #E2E8F0', borderRadius: '12px', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#F8FAFC' }}>
              {['DATA/HORA', 'CAMERA', 'TIPO', 'EPIS', 'STATUS'].map(col => (
                <th key={col} style={{
                  padding: '0.85rem 1rem',
                  textAlign: 'left',
                  fontSize: '0.72rem',
                  fontWeight: '700',
                  color: '#64748B',
                  letterSpacing: '0.05em',
                  borderBottom: '1px solid #E2E8F0'
                }}>
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {ocorrenciasFiltradas.slice(0, 50).map((o, i) => (
              <tr key={o.id} style={{ borderBottom: i < ocorrenciasFiltradas.length - 1 ? '1px solid #F1F5F9' : 'none' }}>
                <td style={{ padding: '0.85rem 1rem', fontSize: '0.85rem', color: '#64748B' }}>
                  {new Date(o.criado_em).toLocaleString('pt-BR')}
                </td>
                <td style={{ padding: '0.85rem 1rem', fontSize: '0.85rem', color: '#003050', fontWeight: '500' }}>
                  {o.camera_nome}
                </td>
                <td style={{ padding: '0.85rem 1rem', fontSize: '0.85rem', color: '#64748B' }}>
                  {o.tipo === 'epi_ausente' ? 'EPI Ausente' : o.tipo === 'conformidade' ? 'Conformidade' : 'Falha de Equipamento'}
                </td>
                <td style={{ padding: '0.85rem 1rem', fontSize: '0.85rem', color: '#64748B' }}>
                  {o.epis_ausentes.length > 0 ? o.epis_ausentes.map(traduzirEpi).join(', ') : '-'}
                </td>
                <td style={{ padding: '0.85rem 1rem' }}>
                  <StatusBadge status={o.status} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}