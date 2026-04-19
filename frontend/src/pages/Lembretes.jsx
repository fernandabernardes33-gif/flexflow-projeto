import { useEffect, useState } from 'react'
import api from '../services/api'
import { Plus, Check, Trash2 } from 'lucide-react'

const empty = { titulo: '', descricao: '', data_prazo: '' }

export default function Lembretes() {
  const [lista, setLista] = useState([])
  const [modal, setModal] = useState(false)
  const [form, setForm] = useState(empty)

  const carregar = () => api.get('/lembretes').then(r => setLista(r.data))
  useEffect(() => { carregar() }, [])

  const salvar = async e => {
    e.preventDefault()
    await api.post('/lembretes', form)
    setModal(false); setForm(empty); carregar()
  }

  const concluir = async id => {
    await api.put(`/lembretes/${id}`, { concluido: true }); carregar()
  }

  const deletar = async id => {
    if (!confirm('Excluir lembrete?')) return
    await api.delete(`/lembretes/${id}`); carregar()
  }

  const pendentes = lista.filter(l => !l.concluido)
  const concluidos = lista.filter(l => l.concluido)

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Lembretes</h1>
        <button onClick={() => setModal(true)}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-primary-dark">
          <Plus size={16} /> Novo Lembrete
        </button>
      </div>

      <div className="space-y-2">
        <h2 className="font-semibold text-gray-600 text-sm">Pendentes ({pendentes.length})</h2>
        {pendentes.map(l => (
          <div key={l.id} className="bg-white rounded-xl p-4 shadow-sm border flex items-center justify-between gap-3">
            <div>
              <p className="font-medium">{l.titulo}</p>
              {l.descricao && <p className="text-sm text-gray-500">{l.descricao}</p>}
              {l.data_prazo && <p className="text-xs text-orange-500 mt-1">Prazo: {new Date(l.data_prazo).toLocaleDateString('pt-BR')}</p>}
            </div>
            <div className="flex gap-2 shrink-0">
              <button onClick={() => concluir(l.id)} title="Concluir"
                className="text-green-500 hover:text-green-700 p-1"><Check size={18} /></button>
              <button onClick={() => deletar(l.id)}
                className="text-red-400 hover:text-red-600 p-1"><Trash2 size={16} /></button>
            </div>
          </div>
        ))}
        {pendentes.length === 0 && <p className="text-sm text-gray-400">Nenhum lembrete pendente.</p>}
      </div>

      {concluidos.length > 0 && (
        <div className="space-y-2">
          <h2 className="font-semibold text-gray-400 text-sm">Concluidos ({concluidos.length})</h2>
          {concluidos.map(l => (
            <div key={l.id} className="bg-white rounded-xl p-4 shadow-sm border flex items-center justify-between gap-3 opacity-60">
              <div>
                <p className="font-medium line-through">{l.titulo}</p>
              </div>
              <button onClick={() => deletar(l.id)} className="text-red-400 hover:text-red-600"><Trash2 size={16} /></button>
            </div>
          ))}
        </div>
      )}

      {modal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl w-full max-w-sm p-6">
            <h2 className="text-lg font-bold mb-4">Novo Lembrete</h2>
            <form onSubmit={salvar} className="space-y-3">
              <input placeholder="Titulo*" required value={form.titulo} onChange={e => setForm({...form,titulo:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <textarea placeholder="Descricao" rows={2} value={form.descricao} onChange={e => setForm({...form,descricao:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <input type="datetime-local" value={form.data_prazo} onChange={e => setForm({...form,data_prazo:e.target.value})}
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
