import { useState } from 'react'
import { User, Save, Check } from 'lucide-react'
import { useAuthStore } from '../hooks/useAuth'

export default function Profile() {
  const { accessToken } = useAuthStore()
  const [saved, setSaved] = useState(false)
  const [form, setForm] = useState({
    name: '',
    email: '',
    field: '',
    level: '',
    country: '',
    year: '',
    bio: '',
  })

  const handleSave = () => {
    // TODO: Connect to PATCH /api/v1/users/me
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const filled = Object.values(form).filter((v) => v && v.toString().trim()).length
  const strength = Math.round((filled / 7) * 100)

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6 backdrop-blur-sm">
        <h2 className="text-xl font-bold mb-1 flex items-center gap-2">
          <User size={20} className="text-blue-400" />
          Student Profile
        </h2>
        <p className="text-sm text-zinc-500 mb-6">
          Complete your profile to get AI-matched scholarships and universities.
        </p>

        {/* Strength Bar */}
        <div className="mb-6 p-4 bg-white/[0.02] rounded-xl border border-white/5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-zinc-400">Profile Strength</span>
            <span className="text-sm font-bold text-blue-400">{strength}%</span>
          </div>
          <div className="w-full bg-white/5 rounded-full h-2">
            <div
              className="bg-gradient-to-r from-blue-500 to-violet-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${strength}%` }}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1.5">Full Name</label>
            <input
              type="text"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="e.g., Alex Chen"
              className="w-full px-4 py-2.5 bg-white/[0.05] border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all placeholder:text-zinc-600"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1.5">Email</label>
            <input
              type="email"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              placeholder="alex@university.edu"
              className="w-full px-4 py-2.5 bg-white/[0.05] border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all placeholder:text-zinc-600"
            />
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1.5">Field of Study</label>
            <select
              value={form.field}
              onChange={(e) => setForm({ ...form, field: e.target.value })}
              className="w-full px-4 py-2.5 bg-white/[0.05] border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all"
            >
              <option value="">Select your field...</option>
              <option value="computer_science">Computer Science</option>
              <option value="engineering">Engineering</option>
              <option value="medicine">Medicine</option>
              <option value="business">Business / Finance</option>
              <option value="physics">Physics</option>
              <option value="artificial_intelligence">Artificial Intelligence</option>
              <option value="data_science">Data Science</option>
              <option value="all_fields">Undecided / All Fields</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1.5">Education Level</label>
            <select
              value={form.level}
              onChange={(e) => setForm({ ...form, level: e.target.value })}
              className="w-full px-4 py-2.5 bg-white/[0.05] border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all"
            >
              <option value="">Select level...</option>
              <option value="high_school">High School</option>
              <option value="bachelor">Bachelor's</option>
              <option value="master">Master's</option>
              <option value="phd">PhD</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1.5">Country</label>
            <select
              value={form.country}
              onChange={(e) => setForm({ ...form, country: e.target.value })}
              className="w-full px-4 py-2.5 bg-white/[0.05] border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all"
            >
              <option value="">Select country...</option>
              <option value="US">United States</option>
              <option value="UK">United Kingdom</option>
              <option value="Canada">Canada</option>
              <option value="Germany">Germany</option>
              <option value="Australia">Australia</option>
              <option value="Bangladesh">Bangladesh</option>
              <option value="India">India</option>
              <option value="global">Other / Global</option>
            </select>
          </div>
          <div>
            <label className="block text-xs font-medium text-zinc-400 mb-1.5">Graduation Year</label>
            <input
              type="number"
              value={form.year}
              onChange={(e) => setForm({ ...form, year: e.target.value })}
              placeholder="2027"
              min="2024"
              max="2035"
              className="w-full px-4 py-2.5 bg-white/[0.05] border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all placeholder:text-zinc-600"
            />
          </div>
          <div className="md:col-span-2">
            <label className="block text-xs font-medium text-zinc-400 mb-1.5">Bio / Academic Background</label>
            <textarea
              value={form.bio}
              onChange={(e) => setForm({ ...form, bio: e.target.value })}
              rows={4}
              placeholder="I am a computer science student passionate about AI and machine learning..."
              className="w-full px-4 py-2.5 bg-white/[0.05] border border-white/10 rounded-lg text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20 transition-all resize-none placeholder:text-zinc-600"
            />
          </div>
        </div>

        <div className="mt-6 flex items-center gap-3">
          <button
            onClick={handleSave}
            className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-violet-600 hover:from-blue-500 hover:to-violet-500 text-white rounded-lg font-medium text-sm transition-all shadow-lg shadow-blue-500/20 flex items-center gap-2"
          >
            {saved ? <Check size={16} /> : <Save size={16} />}
            {saved ? 'Saved!' : 'Save Profile'}
          </button>
        </div>

        {!accessToken && (
          <div className="mt-4 p-4 bg-amber-500/5 border border-amber-500/10 rounded-xl">
            <p className="text-sm text-amber-400">
              You are not logged in. Create an account or log in to save your profile to the cloud.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
