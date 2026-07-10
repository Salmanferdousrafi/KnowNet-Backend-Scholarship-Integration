import { ScholarshipMatch } from '../../types/scholarship';
import { formatDistanceToNow } from 'date-fns';
import { ExternalLink, Calendar, DollarSign, MapPin, GraduationCap, Tag } from 'lucide-react';

interface Props {
  scholarship: ScholarshipMatch;
  showMatch?: boolean;
}

export const ScholarshipCard = ({ scholarship, showMatch = false }: Props) => {
  const urgencyColor = 
    scholarship.urgency_score > 0.8 ? 'text-red-500' :
    scholarship.urgency_score > 0.5 ? 'text-amber-500' : 'text-green-500';

  return (
    <div className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-xl p-5 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-lg text-zinc-900 dark:text-zinc-100 line-clamp-2">
          {scholarship.title}
        </h3>
        {showMatch && (
          <span className="bg-blue-100 text-blue-800 text-xs font-bold px-2 py-1 rounded-full">
            {(scholarship.match_score * 100).toFixed(0)}% Match
          </span>
        )}
      </div>
      
      {scholarship.provider && (
        <p className="text-sm text-zinc-500 dark:text-zinc-400 mb-3">{scholarship.provider}</p>
      )}
      
      <div className="flex flex-wrap gap-3 text-sm text-zinc-600 dark:text-zinc-300 mb-3">
        {scholarship.amount && (
          <span className="flex items-center gap-1">
            <DollarSign size={14} /> {scholarship.amount}
          </span>
        )}
        {scholarship.deadline && (
          <span className={`flex items-center gap-1 ${urgencyColor}`}>
            <Calendar size={14} />
            {formatDistanceToNow(new Date(scholarship.deadline), { addSuffix: true })}
          </span>
        )}
        {scholarship.country_scope?.length > 0 && (
          <span className="flex items-center gap-1">
            <MapPin size={14} /> {scholarship.country_scope.join(', ')}
          </span>
        )}
        {scholarship.education_levels?.length > 0 && (
          <span className="flex items-center gap-1">
            <GraduationCap size={14} /> {scholarship.education_levels.join(', ')}
          </span>
        )}
      </div>
      
      {scholarship.field_tags?.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-3">
          {scholarship.field_tags.map((tag) => (
            <span key={tag} className="bg-zinc-100 dark:bg-zinc-800 text-xs px-2 py-1 rounded-md flex items-center gap-1">
              <Tag size={10} /> {tag}
            </span>
          ))}
        </div>
      )}
      
      {showMatch && (
        <div className="grid grid-cols-3 gap-2 mb-3 text-xs text-zinc-500 dark:text-zinc-400">
          <div>Semantic: {(scholarship.semantic_score * 100).toFixed(0)}%</div>
          <div>Rules: {(scholarship.rule_score * 100).toFixed(0)}%</div>
          <div>Urgency: {(scholarship.urgency_score * 100).toFixed(0)}%</div>
        </div>
      )}
      
      <a
        href={scholarship.source_url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
      >
        View Details <ExternalLink size={14} />
      </a>
    </div>
  );
};
