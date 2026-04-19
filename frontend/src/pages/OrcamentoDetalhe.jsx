import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../services/api'
import { ArrowLeft, FileDown } from 'lucide-react'

const statusColor = {
  PENDENTE: 'bg-orange-100 text-orange-700',
  APROVADO: 'bg-green-100 text-green-700',
  RECUSADO: 'bg-red-100 text-red-700',
}

export default function OrcamentoDetalhe() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [orc, setOrc] = useState(null)

  useEffect(() => { api.get(`/orcamentos/${id}`).then(r => setOrc(r.data)) }, [id])

  const mudarStatus = async status => {
    await api.put(`/orcamentos/${id}`, { status })
    api.get(`/orcamentos/${id}`).then(r => setOrc(r.data))
  }

  if (!orc) return <p className="text-gray-400">Carregando...</p>

  return (
    <div className="space-y-6 max-w-2xl">
      <button onClick={() => navigate('/orcamentos')} className="flex items-center gap-2 text-sm text-primary">
        <ArrowLeft size={16} /> Voltar
      </button>

      <div className="flex items-center justify-between flex-wrap gap-3">
        <h1 className="text-2xl font-bold">ORC-{orc.id}</h1>
        <button onClick={() => window.open(`http://localhost:8000/orcamentos/${id}/pdf`)}
          className="flex items-center gap-2 border border-primary text-primary px-3 py-2 rounded-lg text-sm hover:bg-primary-light">
          <FileDown size={16} /> Exportar PDF
        </button>
      </div>

      <div className="bg-white rounded-xl p-5 shadow-sm border space-y-3">
        <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusColor[orc.status]}`}>{orc.status}</span>
        <p className="text-sm text-gray-600"><strong>Data:</strong> {new Date(orc.data).toLocaleDateString('pt-BR')}</p>
        {orc.validade && <p className="text-sm text-gray-600"><strong>Validade:</strong> {new Date(orc.validade).toLocaleDateString('pt-BR')}</p>}
        {orc.observacoes && <p className="text-sm text-gray-600"><strong>Obs:</strong> {orc.observacoes}</p>}
        <p className="font-bold text-lg">Total: R$ {orc.valor_total.toFixed(2)}</p>
      </div>

      {orc.itens.length > 0 && (
        <div className="bg-white rounded-xl p-5 shadow-sm border">
          <h2 className="font-semibold mb-3">Itens</h2>
          {orc.itens.map(item => (
            <div key={item.id} className="flex justify-between text-sm py-2 border-b last:border-0">
              <span>Item x{item.quantidade}</span>
              <span>R$ {(item.quantidade * item.valor_unitario).toFixed(2)}</span>
            </div>
          ))}
        </div>
      )}

      <div className="bg-white rounded-xl p-5 shadow-sm border">
        <h2 className="font-semibold mb-3">Alterar Status</h2>
        <div className="flex gap-2">
          {['PENDENTE', 'APROVADO', 'RECUSADO'].map(s => (
            <button key={s} onClick={() => mudarStatus(s)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors ${
                orc.status === s ? 'bg-primary text-white border-primary' : 'bg-white text-gray-600 hover:border-primary'}`}>
              {s}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
