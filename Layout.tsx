import { Link, useLocation } from 'react-router-dom'
import { GraduationCap, BookOpen, Search, User, Sparkles } from 'lucide-react'

interface LayoutProps {
  children: React.ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const location = useLocation()

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Sparkles },
    { path: '/scholarships', label: 'Scholarships', icon: GraduationCap },
    { path: '/knowledge', label: 'Knowledge', icon: BookOpen },
    { path: '/profile', label: 'Profile', icon: User },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-zinc-900 to-slate-950">
      <header className="border-b border-white/5 bg-white/[0.02] backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 via-violet-500 to-amber-500 flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/20">
              KX
            </div>
            <div>
              <h1 className="font-bold text-zinc-100 tracking-tight text-sm">KnowNet X</h1>
              <p className="text-xs text-zinc-500">AI Knowledge + Opportunity Finder</p>
            </div>
          </Link>
          <nav className="flex items-center gap-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${
                    isActive
                      ? 'text-blue-400 bg-blue-500/10'
                      : 'text-zinc-400 hover:text-zinc-100 hover:bg-white/5'
                  }`}
                >
                  <item.icon size={16} />
                  <span className="hidden sm:inline">{item.label}</span>
                </Link>
              )
            })}
          </nav>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-8">
        {children}
      </main>
      <footer className="border-t border-white/5 mt-12 py-8 text-center">
        <p className="text-sm text-zinc-600">KnowNet X — AI Knowledge Intelligence + Opportunity Finder</p>
        <p className="text-xs text-zinc-700 mt-1">Built with FastAPI · Claude AI · React · Vite</p>
      </footer>
    </div>
  )
}
