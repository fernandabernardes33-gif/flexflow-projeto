import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../services/api'
import { ArrowLeft } from 'lucide-react'

const statusColor = { ABERTA: 'bg-blue-100 text-blue-700', EM_ANDAMENTO: 'bg-yellow-100 text-yellow-700',
  CONCLUIDA: 'bg-green-100 text-green-700', CANCELADA: 'bg-slate-100 text-slate-600',
  PENDENTE: 'bg-orange-100 text-orange-700', APROVADO: 'bg-green-100 text-green-700', RECUSADO: 'bg-red-100 text-red-700' }

export default function ClienteDetalhe() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [cliente, setCliente] = useState(null)
  const [historico, setHistorico] = useState(null)

  useEffect(() => {
    api.get(`/clientes/${id}`).then(r => setCliente(r.data))
    api.get(`/clientes/${id}/historico`).then(r => setHistorico(r.data))
  }, [id])

  if (!cliente) return <p className="text-slate-400">Carregando...</p>

  return (
    <div className="space-y-6">
      <button onClick={() => navigate('/clientes')} className="flex items-center gap-2 text-sm text-primary">
        <ArrowLeft size={16} /> Voltar
      </button>
      <div className="bg-white rounded-xl p-6 shadow-sm border">
        <h1 className="text-xl font-bold mb-4">{cliente.nome}</h1>
        <div className="grid grid-cols-2 gap-3 text-sm">
          <div><span className="text-slate-400">CPF/CNPJ:</span> <span>{cliente.cpf_cnpj || '-'}</span></div>
          <div><span className="text-slate-400">Telefone:</span> <span>{cliente.telefone || '-'}</span></div>
          <div><span className="text-slate-400">E-mail:</span> <span>{cliente.email || '-'}</span></div>
          <div><span className="text-slate-400">Endereco:</span> <span>{cliente.endereco || '-'}</span></div>
        </div>
      </div>

      {historico && (
        <>
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h2 className="font-semibold mb-3">Ordens de Servico</h2>
            {historico.ordens_servico.length === 0
              ? <p className="text-sm text-slate-400">Nenhuma OS.</p>
              : historico.ordens_servico.map(os => (
                <div key={os.id} className="flex justify-between items-center py-2 border-b last:border-0 text-sm">
                  <span>OS #{os.id}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColor[os.status]}`}>{os.status}</span>
                  <span className="font-medium">R$ {os.valor_total.toFixed(2)}</span>
                </div>
              ))}
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border">
            <h2 className="font-semibold mb-3">Orcamentos</h2>
            {historico.orcamentos.length === 0
              ? <p className="text-sm text-slate-400">Nenhum orcamento.</p>
              : historico.orcamentos.map(orc => (
                <div key={orc.id} className="flex justify-between items-center py-2 border-b last:border-0 text-sm">
                  <span>ORC #{orc.id}</span>
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColor[orc.status]}`}>{orc.status}</span>
                  <span className="font-medium">R$ {orc.valor_total.toFixed(2)}</span>
                </div>
              ))}
          </div>
        </>
      )}
    </div>
  )
}
