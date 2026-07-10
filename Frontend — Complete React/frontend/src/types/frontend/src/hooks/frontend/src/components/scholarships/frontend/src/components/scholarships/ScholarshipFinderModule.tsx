import { useState } from 'react';
import { useScholarships, useScholarshipMatches, useSeedDemoScholarships } from '../../hooks/useScholarships';
import { ScholarshipCard } from './ScholarshipCard';
import { Search, Sparkles, Filter, Loader2 } from 'lucide-react';

type ViewMode = 'all' | 'matches';

export const ScholarshipFinderModule = () => {
  const [viewMode, setViewMode] = useState<ViewMode>('matches');
  const [search, setSearch] = useState('');
  const [field, setField] = useState('');
  
  const { data: allScholarships, isLoading: loadingAll } = useScholarships({
    search: search || undefined,
    field: field || undefined,
    sort_by: 'deadline',
    active_only: true,
  });
  
  const { data: matches, isLoading: loadingMatches } = useScholarshipMatches(50);
  const seedMutation = useSeedDemoScholarships();
  
  const isLoading = viewMode === 'matches' ? loadingMatches : loadingAll;
  const data = viewMode === 'matches' ? matches : allScholarships;
  
  const noData = !isLoading && (!data || data.length === 0);
  
  return (
    <div className="w-full max-w-6xl mx-auto p-4">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <Sparkles size={24} className="text-amber-500" />
            Scholarship & Internship Finder
          </h2>
          <p className="text-zinc-500 dark:text-zinc-400 text-sm mt-1">
            AI-matched opportunities based on your profile
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <button
            onClick={() => setViewMode('matches')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              viewMode === 'matches'
                ? 'bg-blue-600 text-white'
                : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300'
            }`}
          >
            For You
          </button>
          <button
            onClick={() => setViewMode('all')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              viewMode === 'all'
                ? 'bg-blue-600 text-white'
                : 'bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300'
            }`}
          >
            Browse All
          </button>
        </div>
      </div>
      
      {viewMode === 'all' && (
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <div className="relative flex-1">
            <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
            <input
              type="text"
              placeholder="Search scholarships..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="relative sm:w-48">
            <Filter size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-zinc-400" />
            <select
              value={field}
              onChange={(e) => setField(e.target.value)}
              className="w-full pl-9 pr-4 py-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none"
            >
              <option value="">All Fields</option>
              <option value="computer_science">Computer Science</option>
              <option value="engineering">Engineering</option>
              <option value="medicine">Medicine</option>
              <option value="all_fields">All Fields</option>
            </select>
          </div>
        </div>
      )}
      
      {isLoading && (
        <div className="flex items-center justify-center py-20">
          <Loader2 size={32} className="animate-spin text-blue-600" />
        </div>
      )}
      
      {noData && viewMode === 'matches' && (
        <div className="text-center py-20 bg-zinc-50 dark:bg-zinc-900/50 rounded-xl border border-dashed border-zinc-200 dark:border-zinc-700">
          <p className="text-zinc-500 dark:text-zinc-400 mb-4">
            No matches yet. Complete your profile (field, country, education level, bio) to get personalized recommendations.
          </p>
          <button
            onClick={() => seedMutation.mutate()}
            disabled={seedMutation.isPending}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
          >
            {seedMutation.isPending ? 'Loading...' : 'Load Demo Scholarships'}
          </button>
        </div>
      )}
      
      {noData && viewMode === 'all' && (
        <div className="text-center py-20 text-zinc-500 dark:text-zinc-400">
          No scholarships found. Try adjusting filters or check back later.
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {data?.map((scholarship) => (
          <ScholarshipCard
            key={scholarship.id}
            scholarship={scholarship}
            showMatch={viewMode === 'matches'}
          />
        ))}
      </div>
    </div>
  );
};
