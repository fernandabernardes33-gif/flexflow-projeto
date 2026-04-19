import { useEffect, useState } from 'react'
import api from '../services/api'
import { Plus, Trash2, Pencil } from 'lucide-react'

const empty = { nome: '', descricao: '', valor: '' }

export default function Servicos() {
  const [lista, setLista] = useState([])
  const [modal, setModal] = useState(false)
  const [form, setForm] = useState(empty)
  const [editId, setEditId] = useState(null)

  const carregar = () => api.get('/servicos').then(r => setLista(r.data))
  useEffect(() => { carregar() }, [])

  const abrir = (s = null) => {
    setEditId(s?.id || null)
    setForm(s ? { nome: s.nome, descricao: s.descricao || '', valor: s.valor } : empty)
    setModal(true)
  }

  const salvar = async e => {
    e.preventDefault()
    const payload = { ...form, valor: +form.valor }
    if (editId) await api.put(`/servicos/${editId}`, payload)
    else await api.post('/servicos', payload)
    setModal(false); carregar()
  }

  const deletar = async id => {
    if (!confirm('Excluir servico?')) return
    await api.delete(`/servicos/${id}`); carregar()
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Servicos</h1>
        <button onClick={() => abrir()}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-primary-dark">
          <Plus size={16} /> Novo Servico
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {lista.map(s => (
          <div key={s.id} className="bg-white rounded-xl p-5 shadow-sm border">
            <div className="flex justify-between items-start">
              <div>
                <p className="font-semibold">{s.nome}</p>
                {s.descricao && <p className="text-sm text-gray-500 mt-1">{s.descricao}</p>}
                <p className="text-primary font-bold mt-2">R$ {s.valor.toFixed(2)}</p>
              </div>
              <div className="flex gap-1">
                <button onClick={() => abrir(s)} className="text-gray-400 hover:text-primary p-1"><Pencil size={15} /></button>
                <button onClick={() => deletar(s.id)} className="text-gray-400 hover:text-red-500 p-1"><Trash2 size={15} /></button>
              </div>
            </div>
          </div>
        ))}
        {lista.length === 0 && <p className="text-gray-400 text-sm">Nenhum servico cadastrado.</p>}
      </div>

      {modal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl w-full max-w-sm p-6">
            <h2 className="text-lg font-bold mb-4">{editId ? 'Editar' : 'Novo'} Servico</h2>
            <form onSubmit={salvar} className="space-y-3">
              <input placeholder="Nome*" required value={form.nome} onChange={e => setForm({...form,nome:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <input placeholder="Descricao" value={form.descricao} onChange={e => setForm({...form,descricao:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <input placeholder="Valor R$" type="number" step="0.01" required value={form.valor}
                onChange={e => setForm({...form,valor:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setModal(false)}
                  className="flex-1 border rounded-lg py-2 text-sm">Cancelar</button>
                <button type="submit"
                  className="flex-1 bg-primary text-white rounded-lg py-2 text-sm font-medium">Salvar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
