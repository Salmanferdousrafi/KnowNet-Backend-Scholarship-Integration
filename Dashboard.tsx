import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Sparkles, GraduationCap, BookOpen, TrendingUp, Calendar, DollarSign, MapPin } from 'lucide-react'
import { useAuthStore } from '../hooks/useAuth'
import { useScholarshipMatches } from '../hooks/useScholarships'

export default function Dashboard() {
  const { accessToken } = useAuthStore()
  const { data: matches, isLoading } = useScholarshipMatches(5)
  const [stats, setStats] = useState({ scholarships: 0, universities: 0, knowledge: 0 })

  useEffect(() => {
    // Demo stats - replace with real API calls
    setStats({ scholarships: 20, universities: 16, knowledge: 3 })
  }, [])

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="text-center py-10">
        <h2 className="text-4xl font-bold text-gradient mb-4">
          Welcome to KnowNet X
        </h2>
        <p className="text-zinc-400 text-lg max-w-2xl mx-auto">
          AI-powered knowledge intelligence platform with scholarship & university matching.
        </p>
        {!accessToken && (
          <div className="mt-6 flex justify-center gap-3">
            <Link
              to="/profile"
              className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-violet-600 text-white rounded-lg font-medium text-sm hover:from-blue-500 hover:to-violet-500 transition-all shadow-lg shadow-blue-500/20"
            >
              Complete Your Profile
            </Link>
          </div>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/scholarships" className="bg-white/[0.03] border border-white/10 rounded-xl p-6 hover:border-amber-500/30 transition-all group">
          <div className="w-10 h-10 rounded-lg bg-amber-500/10 flex items-center justify-center mb-3 group-hover:bg-amber-500/20 transition-colors">
            <GraduationCap size={20} className="text-amber-400" />
          </div>
          <h3 className="font-semibold text-zinc-100">{stats.scholarships} Scholarships</h3>
          <p className="text-sm text-zinc-500 mt-1">AI-matched opportunities</p>
        </Link>
        <Link to="/knowledge" className="bg-white/[0.03] border border-white/10 rounded-xl p-6 hover:border-emerald-500/30 transition-all group">
          <div className="w-10 h-10 rounded-lg bg-emerald-500/10 flex items-center justify-center mb-3 group-hover:bg-emerald-500/20 transition-colors">
            <BookOpen size={20} className="text-emerald-400" />
          </div>
          <h3 className="font-semibold text-zinc-100">{stats.knowledge} Knowledge Entries</h3>
          <p className="text-sm text-zinc-500 mt-1">Semantic AI search</p>
        </Link>
        <div className="bg-white/[0.03] border border-white/10 rounded-xl p-6 hover:border-blue-500/30 transition-all group">
          <div className="w-10 h-10 rounded-lg bg-blue-500/10 flex items-center justify-center mb-3 group-hover:bg-blue-500/20 transition-colors">
            <TrendingUp size={20} className="text-blue-400" />
          </div>
          <h3 className="font-semibold text-zinc-100">Profile Strength</h3>
          <p className="text-sm text-zinc-500 mt-1">Complete for better matches</p>
        </div>
      </div>

      {/* Top Matches Preview */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-xl font-bold text-zinc-100 flex items-center gap-2">
            <Sparkles size={20} className="text-violet-400" />
            Top AI Matches
          </h3>
          <Link to="/scholarships" className="text-sm text-blue-400 hover:text-blue-300">
            View All →
          </Link>
        </div>
        {isLoading ? (
          <div className="text-center py-10 text-zinc-500">Loading matches...</div>
        ) : matches && matches.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {matches.slice(0, 4).map((match) => (
              <div key={match.id} className="bg-white/[0.03] border border-white/10 rounded-xl p-5 hover:border-white/20 transition-all">
                <div className="flex justify-between items-start mb-2">
                  <h4 className="font-semibold text-zinc-100">{match.title}</h4>
                  <span className="bg-gradient-to-r from-blue-500 to-violet-500 text-white text-xs font-bold px-2 py-1 rounded-full">
                    {(match.match_score * 100).toFixed(0)}% Match
                  </span>
                </div>
                <p className="text-sm text-zinc-500 mb-2">{match.provider}</p>
                <div className="flex gap-3 text-xs text-zinc-400">
                  {match.amount && <span className="flex items-center gap-1"><DollarSign size={12} /> {match.amount}</span>}
                  {match.deadline && <span className="flex items-center gap-1"><Calendar size={12} /> {match.deadline}</span>}
                  <span className="flex items-center gap-1"><MapPin size={12} /> {match.country_scope?.[0]}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-10 bg-white/[0.02] border border-white/5 rounded-xl">
            <p className="text-zinc-500">Complete your profile to see AI-matched scholarships.</p>
            <Link to="/profile" className="mt-3 inline-block px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium">
              Go to Profile
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
