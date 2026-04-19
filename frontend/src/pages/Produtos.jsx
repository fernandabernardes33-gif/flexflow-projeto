import { useEffect, useState } from 'react'
import api from '../services/api'
import { Plus, Trash2, ArrowUp, ArrowDown } from 'lucide-react'

const emptyProd = { nome: '', descricao: '', preco_custo: '', preco_venda: '', quantidade_estoque: 0, quantidade_minima: 1 }

export default function Produtos() {
  const [lista, setLista] = useState([])
  const [modal, setModal] = useState(false)
  const [movModal, setMovModal] = useState(null)
  const [form, setForm] = useState(emptyProd)
  const [mov, setMov] = useState({ tipo: 'ENTRADA', quantidade: 1, observacao: '' })

  const carregar = () => api.get('/produtos').then(r => setLista(r.data))
  useEffect(() => { carregar() }, [])

  const salvar = async e => {
    e.preventDefault()
    await api.post('/produtos', { ...form, preco_custo: +form.preco_custo, preco_venda: +form.preco_venda })
    setModal(false); setForm(emptyProd); carregar()
  }

  const registrarMov = async e => {
    e.preventDefault()
    await api.post('/estoque', { produto_id: movModal.id, ...mov, quantidade: +mov.quantidade })
    setMovModal(null); setMov({ tipo: 'ENTRADA', quantidade: 1, observacao: '' }); carregar()
  }

  const deletar = async id => {
    if (!confirm('Excluir produto?')) return
    await api.delete(`/produtos/${id}`); carregar()
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">Estoque</h1>
        <button onClick={() => setModal(true)}
          className="bg-primary text-white px-4 py-2 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-primary-dark">
          <Plus size={16} /> Novo Produto
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 text-gray-600 text-left">
            <tr>
              <th className="px-4 py-3">Produto</th>
              <th className="px-4 py-3 hidden md:table-cell">Venda</th>
              <th className="px-4 py-3">Estoque</th>
              <th className="px-4 py-3 w-28">Acoes</th>
            </tr>
          </thead>
          <tbody>
            {lista.map(p => (
              <tr key={p.id} className={`border-t hover:bg-gray-50 ${p.quantidade_estoque <= p.quantidade_minima ? 'bg-red-50' : ''}`}>
                <td className="px-4 py-3 font-medium">{p.nome}</td>
                <td className="px-4 py-3 hidden md:table-cell">R$ {p.preco_venda.toFixed(2)}</td>
                <td className="px-4 py-3">
                  <span className={`font-medium ${p.quantidade_estoque <= p.quantidade_minima ? 'text-red-600' : ''}`}>
                    {p.quantidade_estoque}
                  </span>
                </td>
                <td className="px-4 py-3 flex gap-1">
                  <button onClick={() => setMovModal(p)} title="Movimentar"
                    className="text-green-600 hover:text-green-800 p-1"><ArrowUp size={15} /></button>
                  <button onClick={() => deletar(p.id)}
                    className="text-red-400 hover:text-red-600 p-1"><Trash2 size={15} /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {modal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl w-full max-w-md p-6">
            <h2 className="text-lg font-bold mb-4">Novo Produto</h2>
            <form onSubmit={salvar} className="space-y-3">
              <input placeholder="Nome*" required value={form.nome} onChange={e => setForm({...form,nome:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <div className="grid grid-cols-2 gap-3">
                <input placeholder="Preco Custo" type="number" step="0.01" value={form.preco_custo}
                  onChange={e => setForm({...form,preco_custo:e.target.value})}
                  className="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
                <input placeholder="Preco Venda" type="number" step="0.01" value={form.preco_venda}
                  onChange={e => setForm({...form,preco_venda:e.target.value})}
                  className="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
                <input placeholder="Qtd Inicial" type="number" value={form.quantidade_estoque}
                  onChange={e => setForm({...form,quantidade_estoque:+e.target.value})}
                  className="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
                <input placeholder="Qtd Minima" type="number" value={form.quantidade_minima}
                  onChange={e => setForm({...form,quantidade_minima:+e.target.value})}
                  className="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              </div>
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

      {movModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl w-full max-w-sm p-6">
            <h2 className="text-lg font-bold mb-1">Movimentacao de Estoque</h2>
            <p className="text-sm text-gray-500 mb-4">{movModal.nome}</p>
            <form onSubmit={registrarMov} className="space-y-3">
              <select value={mov.tipo} onChange={e => setMov({...mov,tipo:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm">
                <option value="ENTRADA">ENTRADA</option>
                <option value="SAIDA">SAIDA</option>
              </select>
              <input type="number" min="1" placeholder="Quantidade" value={mov.quantidade}
                onChange={e => setMov({...mov,quantidade:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <input placeholder="Observacao" value={mov.observacao}
                onChange={e => setMov({...mov,observacao:e.target.value})}
                className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
              <div className="flex gap-3 pt-2">
                <button type="button" onClick={() => setMovModal(null)}
                  className="flex-1 border rounded-lg py-2 text-sm">Cancelar</button>
                <button type="submit"
                  className="flex-1 bg-primary text-white rounded-lg py-2 text-sm font-medium">Registrar</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
