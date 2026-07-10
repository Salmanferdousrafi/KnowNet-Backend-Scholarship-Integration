import { useState } from 'react'
import { useScholarships, useScholarshipMatches } from '../hooks/useScholarships'
import { Search, Filter, Sparkles } from 'lucide-react'

export default function ScholarshipFinder() {
  const [view, setView] = useState<'matches' | 'all'>('matches')
  const [filters, setFilters] = useState({ search: '', field: '', country: '' })

  const { data: matches, isLoading: loadingMatches } = useScholarshipMatches(50)
  const { data: allScholarships, isLoading: loadingAll } = useScholarships({
    search: filters.search || undefined,
    field: filters.field || undefined,
    country: filters.country || undefined,
    sort_by: 'deadline',
    active_only: true,
  })

  const isLoading = view === 'matches' ? loadingMatches : loadingAll
  const data = view === 'matches' ? matches : allScholarships

  return (
    <div>
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-zinc-100 flex items-center gap-2">
            <Sparkles size={24} className="text-amber-400" />
            Scholarship & Internship Finder
          </h2>
          <p className="text-sm text-zinc-500 mt-1">
            {view === 'matches' ? 'AI-matched opportunities based on your profile' : 'Browse all available scholarships'}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setView('matches')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              view === 'matches'
                ? 'bg-blue-600 text-white'
                : 'bg-white/5 text-zinc-400 hover:text-zinc-100 hover:bg-white/10'
            }`}
          >
            For You
          </button>
          <button
            onClick={() => setView('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              view === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-white/5 text-zinc-400 hover:text-zinc-100 hover:bg-white/10'
            }`}
          >
            Browse All
          </button>
        </div>
      </div>

      {view === 'all' && (
        <div className="flex flex-wrap gap-3 mb-6">
          <div className="relative flex-1 min-w-[200px]">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
            <input
              type="text"
              placeholder="Search scholarships..."
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              className="w-full pl-9 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all placeholder:text-zinc-600"
            />
          </div>
          <select
            value={filters.field}
            onChange={(e) => setFilters({ ...filters, field: e.target.value })}
            className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50"
          >
            <option value="">All Fields</option>
            <option value="computer_science">Computer Science</option>
            <option value="engineering">Engineering</option>
            <option value="medicine">Medicine</option>
            <option value="artificial_intelligence">AI / ML</option>
            <option value="all_fields">All Fields</option>
          </select>
          <select
            value={filters.country}
            onChange={(e) => setFilters({ ...filters, country: e.target.value })}
            className="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50"
          >
            <option value="">All Countries</option>
            <option value="US">USA</option>
            <option value="UK">UK</option>
            <option value="Canada">Canada</option>
            <option value="global">Global</option>
          </select>
        </div>
      )}

      {isLoading && (
        <div className="text-center py-20 text-zinc-500">Loading scholarships...</div>
      )}

      {!isLoading && data && data.length === 0 && (
        <div className="text-center py-20 bg-white/[0.02] border border-white/5 rounded-xl">
          <p className="text-zinc-500">
            {view === 'matches'
              ? 'Complete your profile to get AI-matched scholarships.'
              : 'No scholarships found matching your filters.'}
          </p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {data?.map((scholarship) => (
          <ScholarshipCard key={scholarship.id} scholarship={scholarship} showMatch={view === 'matches'} />
        ))}
      </div>
    </div>
  )
}

function ScholarshipCard({ scholarship, showMatch }: { scholarship: any; showMatch?: boolean }) {
  const daysUntil = scholarship.deadline
    ? Math.ceil((new Date(scholarship.deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24))
    : null

  const urgencyColor =
    !daysUntil || daysUntil < 0
      ? 'text-red-500'
      : daysUntil <= 7
      ? 'text-amber-400'
      : daysUntil <= 30
      ? 'text-yellow-400'
      : 'text-emerald-400'

  return (
    <div className="bg-white/[0.03] border border-white/10 rounded-xl p-5 hover:border-white/20 transition-all hover:shadow-lg hover:shadow-blue-500/5">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-zinc-100">{scholarship.title}</h3>
        {showMatch && (
          <span className="bg-gradient-to-r from-blue-500 to-violet-500 text-white text-xs font-bold px-2.5 py-1 rounded-full">
            {(scholarship.match_score * 100).toFixed(0)}% Match
          </span>
        )}
      </div>
      <p className="text-sm text-zinc-500 mb-3">{scholarship.provider || 'Unknown Provider'}</p>
      <div className="flex flex-wrap gap-3 text-sm text-zinc-400 mb-3">
        {scholarship.amount && (
          <span className="flex items-center gap-1">
            <DollarSign size={14} /> {scholarship.amount}
          </span>
        )}
        {daysUntil !== null && (
          <span className={`flex items-center gap-1 ${urgencyColor}`}>
            <Calendar size={14} />
            {daysUntil < 0 ? 'Expired' : `${daysUntil} days left`}
          </span>
        )}
        <span className="flex items-center gap-1">
          <MapPin size={14} /> {scholarship.country_scope?.join(', ')}
        </span>
      </div>
      {scholarship.field_tags && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {scholarship.field_tags.map((tag: string) => (
            <span key={tag} className="bg-white/5 text-zinc-400 text-xs px-2 py-0.5 rounded-md">
              {tag}
            </span>
          ))}
        </div>
      )}
      {showMatch && (
        <div className="grid grid-cols-3 gap-2 mb-3 text-xs text-zinc-500">
          <div>Semantic: {(scholarship.semantic_score * 100).toFixed(0)}%</div>
          <div>Rules: {(scholarship.rule_score * 100).toFixed(0)}%</div>
          <div>Urgency: {(scholarship.urgency_score * 100).toFixed(0)}%</div>
        </div>
      )}
      <a
        href={scholarship.source_url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 text-sm text-blue-400 hover:text-blue-300 font-medium"
      >
        View Details <ExternalLink size={14} />
      </a>
    </div>
  )
}

import { DollarSign, Calendar, MapPin, ExternalLink } from 'lucide-react'
