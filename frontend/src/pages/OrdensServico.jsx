import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { Plus, Eye } from 'lucide-react'

const statusColor = {
  ABERTA: 'bg-blue-100 text-blue-700',
  EM_ANDAMENTO: 'bg-yellow-100 text-yellow-700',
  CONCLUIDA: 'bg-green-100 text-green-700',
  CANCELADA: 'bg-gray-100 text-gray-600',
}

export default function OrdensServico() {
  const [lista, setLista] = useState([])
  const [statusFiltro, setStatusFiltro] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    const url = statusFiltro ? `/ordens-servico?status=${statusFiltro}` : '/ordens-servico'
    api.get(url).then(r => setLista(r.data))
  }, [statusFiltro])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Ordens de Servico</h1>
        <button onClick={() => navigate('/ordens-servico/nova')}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-primary-dark">
          <Plus size={16} /> Nova OS
        </button>
      </div>

      <div className="flex gap-2 flex-wrap">
        {['', 'ABERTA', 'EM_ANDAMENTO', 'CONCLUIDA', 'CANCELADA'].map(s => (
          <button key={s} onClick={() => setStatusFiltro(s)}
            className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors ${
              statusFiltro === s ? 'bg-primary text-white border-primary' : 'bg-white text-gray-600 hover:border-primary'}`}>
            {s || 'Todas'}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-600 text-left">
            <tr>
              <th className="px-4 py-3">#</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3 hidden md:table-cell">Abertura</th>
              <th className="px-4 py-3 hidden lg:table-cell">Total</th>
              <th className="px-4 py-3 w-16">Ver</th>
            </tr>
          </thead>
          <tbody>
            {lista.map(os => (
              <tr key={os.id} className="border-t hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">OS-{os.id}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColor[os.status]}`}>{os.status}</span>
                </td>
                <td className="px-4 py-3 hidden md:table-cell">
                  {new Date(os.data_abertura).toLocaleDateString('pt-BR')}
                </td>
                <td className="px-4 py-3 hidden lg:table-cell">R$ {os.valor_total.toFixed(2)}</td>
                <td className="px-4 py-3">
                  <button onClick={() => navigate(`/ordens-servico/${os.id}`)}
                    className="text-primary hover:text-primary-dark"><Eye size={16} /></button>
                </td>
              </tr>
            ))}
            {lista.length === 0 && (
              <tr><td colSpan={5} className="px-4 py-8 text-center text-gray-400">Nenhuma OS encontrada.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
