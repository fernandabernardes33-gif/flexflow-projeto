import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { Plus, Search, Eye, Trash2 } from 'lucide-react'

const empty = { nome: '', cpf_cnpj: '', telefone: '', email: '', endereco: '' }

export default function Clientes() {
  const [lista, setLista] = useState([])
  const [filtro, setFiltro] = useState('')
  const [modal, setModal] = useState(false)
  const [form, setForm] = useState(empty)
  const navigate = useNavigate()

  const carregar = () => api.get('/clientes').then(r => setLista(r.data))
  useEffect(() => { carregar() }, [])

  const salvar = async e => {
    e.preventDefault()
    await api.post('/clientes', form)
    setModal(false)
    setForm(empty)
    carregar()
  }

  const deletar = async id => {
    if (!confirm('Excluir cliente?')) return
    await api.delete(`/clientes/${id}`)
    carregar()
  }

  const filtrados = lista.filter(c =>
    c.nome.toLowerCase().includes(filtro.toLowerCase()) ||
    (c.telefone || '').includes(filtro)
  )

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Clientes</h1>
        <button onClick={() => setModal(true)}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-primary-dark">
          <Plus size={16} /> Novo Cliente
        </button>
      </div>

      <div className="relative">
        <Search size={16} className="absolute left-3 top-3 text-slate-400" />
        <input value={filtro} onChange={e => setFiltro(e.target.value)}
          placeholder="Buscar por nome ou telefone..."
          className="w-full border rounded-lg pl-9 pr-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600 text-left">
            <tr>
              <th className="px-4 py-3">Nome</th>
              <th className="px-4 py-3 hidden md:table-cell">Telefone</th>
              <th className="px-4 py-3 hidden lg:table-cell">E-mail</th>
              <th className="px-4 py-3 w-24">Acoes</th>
            </tr>
          </thead>
          <tbody>
            {filtrados.map(c => (
              <tr key={c.id} className="border-t hover:bg-slate-50">
                <td className="px-4 py-3 font-medium">{c.nome}</td>
                <td className="px-4 py-3 hidden md:table-cell">{c.telefone || '-'}</td>
                <td className="px-4 py-3 hidden lg:table-cell">{c.email || '-'}</td>
                <td className="px-4 py-3 flex gap-2">
                  <button onClick={() => navigate(`/clientes/${c.id}`)}
                    className="text-primary hover:text-primary-dark"><Eye size={16} /></button>
                  <button onClick={() => deletar(c.id)}
                    className="text-red-400 hover:text-red-600"><Trash2 size={16} /></button>
                </td>
              </tr>
            ))}
            {filtrados.length === 0 && (
              <tr><td colSpan={4} className="px-4 py-8 text-center text-slate-400">Nenhum cliente encontrado.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {modal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl w-full max-w-md p-6">
            <h2 className="text-lg font-bold mb-4">Novo Cliente</h2>
            <form onSubmit={salvar} className="space-y-3">
              {[['nome','Nome*'],['cpf_cnpj','CPF/CNPJ'],['telefone','Telefone'],['email','E-mail'],['endereco','Endereco']].map(([k,l]) => (
                <div key={k}>
                  <label className="text-sm font-medium text-slate-600">{l}</label>
                  <input value={form[k]} onChange={e => setForm({...form,[k]:e.target.value})}
                    required={k==='nome'}
                    className="w-full border rounded-lg px-3 py-2 text-sm mt-1 focus:outline-none focus:ring-2 focus:ring-primary" />
                </div>
              ))}
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
