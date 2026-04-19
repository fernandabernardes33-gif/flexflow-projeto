import { useEffect, useState } from 'react'
import api from '../services/api'
import { ClipboardList, DollarSign, TrendingUp, AlertTriangle, Bell } from 'lucide-react'

const Card = ({ label, value, icon: Icon, color }) => (
  <div className="bg-white rounded-xl p-5 shadow-sm border flex items-center gap-4">
    <div className={`p-3 rounded-lg ${color}`}><Icon size={22} className="text-white" /></div>
    <div>
      <p className="text-sm text-gray-500">{label}</p>
      <p className="text-2xl font-bold text-gray-800">{value}</p>
    </div>
  </div>
)

export default function Painel() {
  const [dados, setDados] = useState(null)

  useEffect(() => {
    api.get('/painel').then(r => setDados(r.data)).catch(() => {})
  }, [])

  if (!dados) return <p className="text-gray-400">Carregando...</p>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">Painel</h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <Card label="OS Abertas" value={dados.os_abertas} icon={ClipboardList} color="bg-blue-500" />
        <Card label="OS Em Andamento" value={dados.os_andamento} icon={ClipboardList} color="bg-yellow-500" />
        <Card label="OS Concluidas (mes)" value={dados.os_concluidas_mes} icon={ClipboardList} color="bg-green-500" />
        <Card label="Receita do Mes" value={`R$ ${dados.receita_mes.toFixed(2)}`} icon={TrendingUp} color="bg-emerald-500" />
        <Card label="Despesas do Mes" value={`R$ ${dados.despesas_mes.toFixed(2)}`} icon={DollarSign} color="bg-red-500" />
        <Card label="Saldo do Mes" value={`R$ ${dados.saldo_mes.toFixed(2)}`} icon={DollarSign} color="bg-indigo-500" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-sm border">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle size={18} className="text-orange-500" />
            <h2 className="font-semibold">Estoque Baixo</h2>
          </div>
          {dados.estoque_baixo.length === 0
            ? <p className="text-sm text-gray-400">Nenhum produto abaixo do minimo.</p>
            : dados.estoque_baixo.map(p => (
              <div key={p.id} className="flex justify-between text-sm py-2 border-b last:border-0">
                <span>{p.nome}</span>
                <span className="text-red-500 font-medium">{p.estoque} / min {p.minimo}</span>
              </div>
            ))}
        </div>

        <div className="bg-white rounded-xl p-5 shadow-sm border">
          <div className="flex items-center gap-2 mb-4">
            <Bell size={18} className="text-blue-500" />
            <h2 className="font-semibold">Lembretes Pendentes</h2>
          </div>
          {dados.lembretes_pendentes.length === 0
            ? <p className="text-sm text-gray-400">Nenhum lembrete pendente.</p>
            : dados.lembretes_pendentes.map(l => (
              <div key={l.id} className="py-2 border-b last:border-0">
                <p className="text-sm font-medium">{l.titulo}</p>
                {l.data_prazo && <p className="text-xs text-gray-400">{new Date(l.data_prazo).toLocaleDateString('pt-BR')}</p>}
              </div>
            ))}
        </div>
      </div>
    </div>
  )
}
