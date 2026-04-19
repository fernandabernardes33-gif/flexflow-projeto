import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { Plus, Eye } from 'lucide-react'

const statusColor = {
  PENDENTE: 'bg-orange-100 text-orange-700',
  APROVADO: 'bg-green-100 text-green-700',
  RECUSADO: 'bg-red-100 text-red-700',
}

export default function Orcamentos() {
  const [lista, setLista] = useState([])
  const navigate = useNavigate()

  useEffect(() => { api.get('/orcamentos').then(r => setLista(r.data)) }, [])

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Orcamentos</h1>
        <button onClick={() => navigate('/orcamentos/novo')}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-primary-dark">
          <Plus size={16} /> Novo Orcamento
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-600 text-left">
            <tr>
              <th className="px-4 py-3">#</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3 hidden md:table-cell">Data</th>
              <th className="px-4 py-3 hidden lg:table-cell">Total</th>
              <th className="px-4 py-3 w-16">Ver</th>
            </tr>
          </thead>
          <tbody>
            {lista.map(orc => (
              <tr key={orc.id} className="border-t hover:bg-gray-50">
                <td className="px-4 py-3 font-medium">ORC-{orc.id}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${statusColor[orc.status]}`}>{orc.status}</span>
                </td>
                <td className="px-4 py-3 hidden md:table-cell">{new Date(orc.data).toLocaleDateString('pt-BR')}</td>
                <td className="px-4 py-3 hidden lg:table-cell">R$ {orc.valor_total.toFixed(2)}</td>
                <td className="px-4 py-3">
                  <button onClick={() => navigate(`/orcamentos/${orc.id}`)} className="text-primary hover:text-primary-dark"><Eye size={16} /></button>
                </td>
              </tr>
            ))}
            {lista.length === 0 && (
              <tr><td colSpan={5} className="px-4 py-8 text-center text-gray-400">Nenhum orcamento encontrado.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
