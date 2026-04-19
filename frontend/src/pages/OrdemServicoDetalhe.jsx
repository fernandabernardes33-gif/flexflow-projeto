import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../services/api'
import { ArrowLeft, FileDown } from 'lucide-react'

const statusColor = {
  ABERTA: 'bg-blue-100 text-blue-700', EM_ANDAMENTO: 'bg-yellow-100 text-yellow-700',
  CONCLUIDA: 'bg-green-100 text-green-700', CANCELADA: 'bg-gray-100 text-gray-600',
}

export default function OrdemServicoDetalhe() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [os, setOs] = useState(null)

  useEffect(() => { api.get(`/ordens-servico/${id}`).then(r => setOs(r.data)) }, [id])

  const mudarStatus = async status => {
    await api.put(`/ordens-servico/${id}`, { status })
    api.get(`/ordens-servico/${id}`).then(r => setOs(r.data))
  }

  const exportarPdf = () => {
    const token = localStorage.getItem('token')
    window.open(`http://localhost:8000/ordens-servico/${id}/pdf?token=${token}`)
  }

  if (!os) return <p className="text-gray-400">Carregando...</p>

  return (
    <div className="space-y-6 max-w-2xl">
      <button onClick={() => navigate('/ordens-servico')} className="flex items-center gap-2 text-sm text-primary">
        <ArrowLeft size={16} /> Voltar
      </button>

      <div className="flex items-center justify-between flex-wrap gap-3">
        <h1 className="text-2xl font-bold">OS-{os.id}</h1>
        <div className="flex gap-2">
          <button onClick={exportarPdf}
            className="flex items-center gap-2 border border-primary text-primary px-3 py-2 rounded-lg text-sm hover:bg-primary-light">
            <FileDown size={16} /> Exportar PDF
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl p-5 shadow-sm border space-y-3">
        <div className="flex items-center gap-3">
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColor[os.status]}`}>{os.status}</span>
        </div>
        <p className="text-sm text-gray-600"><strong>Abertura:</strong> {new Date(os.data_abertura).toLocaleDateString('pt-BR')}</p>
        {os.data_previsao && <p className="text-sm text-gray-600"><strong>Previsao:</strong> {new Date(os.data_previsao).toLocaleDateString('pt-BR')}</p>}
        {os.descricao_problema && <p className="text-sm text-gray-600"><strong>Problema:</strong> {os.descricao_problema}</p>}
        {os.observacoes && <p className="text-sm text-gray-600"><strong>Obs:</strong> {os.observacoes}</p>}
        <p className="font-bold text-lg">Total: R$ {os.valor_total.toFixed(2)}</p>
      </div>

      {os.itens.length > 0 && (
        <div className="bg-white rounded-xl p-5 shadow-sm border">
          <h2 className="font-semibold mb-3">Itens</h2>
          {os.itens.map(item => (
            <div key={item.id} className="flex justify-between text-sm py-2 border-b last:border-0">
              <span>Item #{item.produto_id || item.servico_id} x{item.quantidade}</span>
              <span>R$ {(item.quantidade * item.valor_unitario).toFixed(2)}</span>
            </div>
          ))}
        </div>
      )}

      <div className="bg-white rounded-xl p-5 shadow-sm border">
        <h2 className="font-semibold mb-3">Alterar Status</h2>
        <div className="flex gap-2 flex-wrap">
          {['ABERTA', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA'].map(s => (
            <button key={s} onClick={() => mudarStatus(s)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors ${
                os.status === s ? 'bg-primary text-white border-primary' : 'bg-white text-gray-600 hover:border-primary'}`}>
              {s}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
