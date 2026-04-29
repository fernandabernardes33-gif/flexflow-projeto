import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'
import { ArrowLeft, Plus, Trash2 } from 'lucide-react'

export default function OrdemServicoNova() {
  const navigate = useNavigate()
  const [clientes, setClientes] = useState([])
  const [servicos, setServicos] = useState([])
  const [produtos, setProdutos] = useState([])
  const [form, setForm] = useState({ cliente_id: '', descricao_problema: '', data_previsao: '', observacoes: '' })
  const [itens, setItens] = useState([])
  const [novoItem, setNovoItem] = useState({ tipo: 'servico', ref_id: '', quantidade: 1, valor_unitario: '' })

  useEffect(() => {
    api.get('/clientes').then(r => setClientes(r.data))
    api.get('/servicos').then(r => setServicos(r.data))
    api.get('/produtos').then(r => setProdutos(r.data))
  }, [])

  const addItem = () => {
    if (!novoItem.ref_id || !novoItem.valor_unitario) return
    const lista = novoItem.tipo === 'servico' ? servicos : produtos
    const ref = lista.find(x => x.id === +novoItem.ref_id)
    setItens([...itens, {
      tipo: novoItem.tipo,
      [novoItem.tipo === 'servico' ? 'servico_id' : 'produto_id']: +novoItem.ref_id,
      nome: ref?.nome || '',
      quantidade: +novoItem.quantidade,
      valor_unitario: +novoItem.valor_unitario,
    }])
    setNovoItem({ tipo: 'servico', ref_id: '', quantidade: 1, valor_unitario: '' })
  }

  const total = itens.reduce((s, i) => s + i.quantidade * i.valor_unitario, 0)

  const salvar = async e => {
    e.preventDefault()
    const payload = {
      ...form,
      cliente_id: +form.cliente_id,
      itens: itens.map(({ nome, tipo, ...rest }) => rest),
    }
    const { data } = await api.post('/ordens-servico', payload)
    navigate(`/ordens-servico/${data.id}`)
  }

  return (
    <div className="space-y-6 max-w-2xl">
      <button onClick={() => navigate('/ordens-servico')} className="flex items-center gap-2 text-sm text-primary">
        <ArrowLeft size={16} /> Voltar
      </button>
      <h1 className="text-2xl font-bold">Nova Ordem de Servico</h1>

      <form onSubmit={salvar} className="space-y-4">
        <div className="bg-white rounded-xl p-5 shadow-sm border space-y-3">
          <h2 className="font-semibold text-slate-600">Dados Gerais</h2>
          <select required value={form.cliente_id} onChange={e => setForm({...form,cliente_id:e.target.value})}
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary">
            <option value="">Selecione o cliente*</option>
            {clientes.map(c => <option key={c.id} value={c.id}>{c.nome}</option>)}
          </select>
          <textarea placeholder="Descricao do problema" value={form.descricao_problema}
            onChange={e => setForm({...form,descricao_problema:e.target.value})}
            rows={3} className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          <input type="datetime-local" value={form.data_previsao}
            onChange={e => setForm({...form,data_previsao:e.target.value})}
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
          <textarea placeholder="Observacoes" value={form.observacoes}
            onChange={e => setForm({...form,observacoes:e.target.value})}
            rows={2} className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary" />
        </div>

        <div className="bg-white rounded-xl p-5 shadow-sm border space-y-3">
          <h2 className="font-semibold text-slate-600">Itens</h2>
          <div className="flex gap-2 flex-wrap">
            <select value={novoItem.tipo} onChange={e => setNovoItem({...novoItem,tipo:e.target.value,ref_id:''})}
              className="border rounded-lg px-3 py-2 text-sm">
              <option value="servico">Servico</option>
              <option value="produto">Produto</option>
            </select>
            <select value={novoItem.ref_id} onChange={e => {
              const lista = novoItem.tipo === 'servico' ? servicos : produtos
              const ref = lista.find(x => x.id === +e.target.value)
              setNovoItem({...novoItem,ref_id:e.target.value,valor_unitario:ref?.valor||ref?.preco_venda||''})
            }} className="flex-1 border rounded-lg px-3 py-2 text-sm">
              <option value="">Selecione...</option>
              {(novoItem.tipo === 'servico' ? servicos : produtos).map(x =>
                <option key={x.id} value={x.id}>{x.nome}</option>)}
            </select>
            <input type="number" min="1" placeholder="Qtd" value={novoItem.quantidade}
              onChange={e => setNovoItem({...novoItem,quantidade:e.target.value})}
              className="w-20 border rounded-lg px-3 py-2 text-sm" />
            <input type="number" step="0.01" placeholder="Valor" value={novoItem.valor_unitario}
              onChange={e => setNovoItem({...novoItem,valor_unitario:e.target.value})}
              className="w-28 border rounded-lg px-3 py-2 text-sm" />
            <button type="button" onClick={addItem}
              className="bg-primary text-white px-3 py-2 rounded-lg"><Plus size={16} /></button>
          </div>
          {itens.map((item, i) => (
            <div key={i} className="flex justify-between items-center py-2 border-b text-sm">
              <span>{item.nome} x{item.quantidade}</span>
              <span>R$ {(item.quantidade * item.valor_unitario).toFixed(2)}</span>
              <button type="button" onClick={() => setItens(itens.filter((_, j) => j !== i))}
                className="text-red-400 hover:text-red-600"><Trash2 size={14} /></button>
            </div>
          ))}
          <div className="flex justify-between font-bold pt-2">
            <span>Total</span>
            <span>R$ {total.toFixed(2)}</span>
          </div>
        </div>

        <button type="submit"
          className="w-full bg-primary text-white py-3 rounded-lg font-semibold hover:bg-primary-dark">
          Salvar OS
        </button>
      </form>
    </div>
  )
}
