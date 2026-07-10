import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ScholarshipFinder from './pages/ScholarshipFinder'
import KnowledgeBase from './pages/KnowledgeBase'
import Profile from './pages/Profile'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/scholarships" element={<ScholarshipFinder />} />
        <Route path="/knowledge" element={<KnowledgeBase />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Layout>
  )
}

export default App
