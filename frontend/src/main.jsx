import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import './index.css'
import { AuthProvider, AuthContext } from './context/AuthContext'
import { useContext } from 'react'

import Layout from './components/Layout'
import Login from './pages/Login'
import Painel from './pages/Painel'
import Clientes from './pages/Clientes'
import ClienteDetalhe from './pages/ClienteDetalhe'
import Produtos from './pages/Produtos'
import Servicos from './pages/Servicos'
import OrdensServico from './pages/OrdensServico'
import OrdemServicoNova from './pages/OrdemServicoNova'
import OrdemServicoDetalhe from './pages/OrdemServicoDetalhe'
import Orcamentos from './pages/Orcamentos'
import OrcamentoNovo from './pages/OrcamentoNovo'
import OrcamentoDetalhe from './pages/OrcamentoDetalhe'
import Financeiro from './pages/Financeiro'
import Lembretes from './pages/Lembretes'

function Guard({ children }) {
  const { user, loading } = useContext(AuthContext)
  if (loading) return null
  return user ? children : <Navigate to="/login" replace />
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<Guard><Layout /></Guard>}>
            <Route index element={<Painel />} />
            <Route path="clientes" element={<Clientes />} />
            <Route path="clientes/:id" element={<ClienteDetalhe />} />
            <Route path="produtos" element={<Produtos />} />
            <Route path="servicos" element={<Servicos />} />
            <Route path="ordens-servico" element={<OrdensServico />} />
            <Route path="ordens-servico/nova" element={<OrdemServicoNova />} />
            <Route path="ordens-servico/:id" element={<OrdemServicoDetalhe />} />
            <Route path="orcamentos" element={<Orcamentos />} />
            <Route path="orcamentos/novo" element={<OrcamentoNovo />} />
            <Route path="orcamentos/:id" element={<OrcamentoDetalhe />} />
            <Route path="financeiro" element={<Financeiro />} />
            <Route path="lembretes" element={<Lembretes />} />
          </Route>
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
)
