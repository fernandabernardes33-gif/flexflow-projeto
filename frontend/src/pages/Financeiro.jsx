import { useEffect, useState } from 'react'
import api from '../services/api'
import { Plus, Trash2 } from 'lucide-react'

const empty = { tipo: 'ENTRADA', valor: '', descricao: '', categoria: '' }

export default function Financeiro() {
  const [lista, setLista] = useState([])
  const [modal, setModal] = useState(false)
  const [form, setForm] = useState(empty)

  const carregar = () => api.get('/financeiro').then(r => setLista(r.data))
  useEffect(() => { carregar() }, [])

  const salvar = async e => {
    e.preventDefault()
    await api.post('/financeiro', { ...form, valor: +form.valor })
    setModal(false); setForm(empty); carregar()
  }

  const deletar = async id => {
    if (!confirm('Excluir lancamento?')) return
    await api.delete(`/financeiro/${id}`); carregar()
  }

  const receita = lista.filter(m => m.tipo === 'ENTRADA').reduce((s, m) => s + m.valor, 0)
  const despesas = lista.filter(m => m.tipo === 'SAIDA').reduce((s, m) => s + m.valor, 0)

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Financeiro</h1>
        <button onClick={() => setModal(true)}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-primary-dark">
          <Plus size={16} /> Novo Lancamento
        </button>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-xl p-4 shadow-sm border text-center">
          <p className="text-sm text-slate-400">Receitas</p>
          <p className="text-xl font-bold text-green-600">R$ {receita.toFixed(2)}</p>
        </div>
        <div className="bg-white rounded-xl p-4 shadow-sm border text-center">
          <p className="text-sm text-slate-400">Despesas</p>
          <p className="text-xl font-bold text-red-500">R$ {despesas.toFixed(2)}</p>
        </div>
        <div className="bg-white rounded-xl p-4 shadow-sm border text-center">
          <p className="text-sm text-slate-400">Saldo</p>
          <p className={`text-xl font-bold ${receita - despesas >= 0 ? 'text-primary' : 'text-red-500'}`}>
            R$ {(receita - despesas).toFixed(2)}
          </p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600 text-left">
            <tr>
              <th className="px-4 py-3">Descricao</th>
              <th className="px-4 py-3">Tipo</th>
              <th className="px-4 py-3 hidden md:table-cell">Categoria</th>
              <th className="px-4 py-3">Valor</th>
              <th className="px-4 py-3 hidden md:table-cell">Data</th>
              <th className="px-4 py-3 w-12"></th>
            </tr>
          </thead>
          <tbody>
            {lista.map(m => (
              <tr key={m.id} className="border-t hover:bg-slate-50">
                <td className="px-4 py-3">{m.descricao || '-'}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                    m.tipo === 'ENTRADA' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                    {m.tipo}
                  </span>
                </td>
                <td className="px-4 py-3 hidden md:table-cell">{m.categoria || '-'}</td>
                <td className={`px-4 py-3 font-medium ${m.tipo === 'ENTRADA' ? 'text-green-600' : 'text-red-500'}`}>
                  R$ {m.valor.toFixed(2)}
                </td>
                <td className="px-4 py-3 hidden md:table-cell">{new Date(m.data).toLocaleDateString('pt-BR')}</td>
                <td className="px-4 py-3">
                  <button onClick={() => deletar(m.id)} className="text-red-400 hover:text-red-600"><Trash2 size={15} /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {modal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl w-full max-w-sm p-6">
            <h2 className="text-lg font-bold mb-4">Novo Lancamento</h2>
            <form onSubmit={salvar} className="space-y-3">
              <select value={form.tipo} onChange={e => setForm({...form,tipo:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm">
                <option value="ENTRADA">ENTRADA</option>
                <option value="SAIDA">SAIDA</option>
              </select>
              <input placeholder="Valor R$*" type="number" step="0.01" required value={form.valor}
                onChange={e => setForm({...form,valor:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <input placeholder="Descricao" value={form.descricao} onChange={e => setForm({...form,descricao:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <input placeholder="Categoria" value={form.categoria} onChange={e => setForm({...form,categoria:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setModal(false)} className="flex-1 border rounded-lg py-2 text-sm">Cancelar</button>
                <button type="submit" className="flex-1 bg-primary text-white rounded-lg py-2 text-sm font-medium">Salvar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
