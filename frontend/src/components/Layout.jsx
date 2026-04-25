import { useState, useContext } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { AuthContext } from '../context/AuthContext'
import {
  LayoutDashboard, Users, Package, Wrench, ClipboardList,
  FileText, DollarSign, Bell, LogOut, Menu, X, Monitor
} from 'lucide-react'

const nav = [
  { to: '/', icon: LayoutDashboard, label: 'Painel' },
  { to: '/clientes', icon: Users, label: 'Clientes' },
  { to: '/produtos', icon: Package, label: 'Estoque' },
  { to: '/servicos', icon: Wrench, label: 'Servicos' },
  { to: '/ordens-servico', icon: ClipboardList, label: 'Ordens de Servico' },
  { to: '/orcamentos', icon: FileText, label: 'Orcamentos' },
  { to: '/financeiro', icon: DollarSign, label: 'Financeiro' },
  { to: '/lembretes', icon: Bell, label: 'Lembretes' },
]

export default function Layout() {
  const { user, logout } = useContext(AuthContext)
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)

  const handleLogout = () => { logout(); navigate('/login') }

  const Sidebar = ({ mobile = false }) => (
    <aside className={`bg-primary text-white flex flex-col ${mobile ? 'w-64' : 'w-64 hidden md:flex'} h-full`}>
      <div className="p-5 border-b border-blue-700 flex items-center gap-2">
        <Monitor size={22} />
        <span className="font-bold text-lg">SIGIT</span>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {nav.map(({ to, icon: Icon, label }) => (
          <NavLink key={to} to={to} end={to === '/'}
            onClick={() => setOpen(false)}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                isActive ? 'bg-white/20 font-semibold' : 'hover:bg-white/10'
              }`}>
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-blue-700">
        <p className="text-xs text-blue-200 mb-2">{user?.nome || 'Usuario'}</p>
        <button onClick={handleLogout}
          className="flex items-center gap-2 text-sm hover:text-red-300 transition-colors">
          <LogOut size={16} /> Sair
        </button>
      </div>
    </aside>
  )

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />

      {open && (
        <div className="fixed inset-0 z-50 flex md:hidden">
          <div className="absolute inset-0 bg-black/50" onClick={() => setOpen(false)} />
          <div className="relative z-10 h-full">
            <Sidebar mobile />
          </div>
        </div>
      )}

      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-white border-b px-4 py-3 flex items-center gap-3 md:hidden">
          <button onClick={() => setOpen(true)}>
            <Menu size={22} />
          </button>
          <span className="font-bold text-primary">SIGIT</span>
        </header>
        <main className="flex-1 overflow-auto p-4 md:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
