import { useState } from 'react'
import { Search, BookOpen } from 'lucide-react'

const demoEntries = [
  {
    id: 1,
    title: 'Transformer Architecture Deep Dive',
    category: 'AI / ML',
    content: 'The transformer architecture introduced in "Attention Is All You Need" revolutionized NLP by replacing recurrent layers with self-attention mechanisms...',
    source: 'arXiv',
    date: '2 days ago',
    relevance: 94,
  },
  {
    id: 2,
    title: 'Fulbright Application Guide 2026',
    category: 'Scholarships',
    content: 'Complete walkthrough of the Fulbright Foreign Student Program application, including personal statement tips, recommendation letter strategy, and interview preparation...',
    source: 'Fulbright Official',
    date: '1 week ago',
    relevance: 88,
  },
  {
    id: 3,
    title: 'GRE Quantitative Reasoning Strategies',
    category: 'Test Prep',
    content: 'Advanced strategies for the GRE quantitative section, including time management techniques, common trap questions, and calculator shortcuts...',
    source: 'ETS',
    date: '3 weeks ago',
    relevance: 82,
  },
]

export default function KnowledgeBase() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(demoEntries)

  const handleSearch = () => {
    if (!query) {
      setResults(demoEntries)
      return
    }
    const q = query.toLowerCase()
    const filtered = demoEntries.map((entry) => {
      const titleMatch = entry.title.toLowerCase().includes(q)
      const contentMatch = entry.content.toLowerCase().includes(q)
      const relevance = (titleMatch ? 50 : 0) + (contentMatch ? 30 : 0) + Math.floor(Math.random() * 20)
      return { ...entry, relevance: Math.min(99, relevance) }
    }).filter((e) => e.relevance > 10)
    setResults(filtered)
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-zinc-100 flex items-center gap-2">
          <BookOpen size={24} className="text-emerald-400" />
          Knowledge Base
        </h2>
        <p className="text-sm text-zinc-500 mt-1">Semantic AI search across your knowledge entries</p>
      </div>

      <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 mb-6">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500" />
            <input
              type="text"
              placeholder="Ask anything about your knowledge..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/10 rounded-xl text-sm focus:outline-none focus:border-emerald-500/50 focus:ring-1 focus:ring-emerald-500/20 transition-all placeholder:text-zinc-600"
            />
          </div>
          <button
            onClick={handleSearch}
            className="px-6 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl font-medium text-sm transition-all flex items-center gap-2"
          >
            <Search size={16} />
            AI Search
          </button>
        </div>
      </div>

      <div className="space-y-3">
        {results.map((entry) => (
          <div key={entry.id} className="bg-white/[0.03] border border-white/10 rounded-xl p-5 hover:border-white/20 transition-colors">
            <div className="flex items-start justify-between mb-2">
              <h3 className="font-semibold text-zinc-100">{entry.title}</h3>
              <span className="text-xs text-emerald-400 bg-emerald-500/10 px-2 py-1 rounded-full">{entry.category}</span>
            </div>
            <p className="text-sm text-zinc-400 line-clamp-2 mb-3">{entry.content}</p>
            <div className="flex items-center gap-3 text-xs text-zinc-500">
              <span>Source: {entry.source}</span>
              <span>•</span>
              <span>Added {entry.date}</span>
              <span>•</span>
              <span className="text-emerald-400">Relevance: {entry.relevance}%</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
