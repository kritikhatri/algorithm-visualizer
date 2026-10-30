import { useEffect } from 'react'
import { Route, Routes, useLocation } from 'react-router-dom'
import './App.css'

import { useAuth } from './auth'
import Navbar from './components/Navbar'
import AuthModal from './components/AuthModal'
import Home from './pages/Home'
import Topic from './pages/Topic'
import Problems from './pages/Problems'
import Problem from './pages/Problem'
import Playground from './pages/Playground'
import Flashcards from './pages/Flashcards'
import Race from './pages/Race'
import CheatSheet from './pages/CheatSheet'
import Patterns from './pages/Patterns'
import Dashboard from './pages/Dashboard'
import NotFound from './pages/NotFound'

function App() {
  const { authOpen } = useAuth()
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [pathname])

  return (
    <div className="app">
      <Navbar />

      <div className="aurora" aria-hidden="true"><i /><i /><i /></div>

      <main className="page" key={pathname}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/topics/:topicId" element={<Topic />} />
          <Route path="/topics/:topicId/:tab" element={<Topic />} />
          <Route path="/problems" element={<Problems />} />
          <Route path="/problems/:problemId" element={<Problem />} />
          <Route path="/playground" element={<Playground />} />
          <Route path="/flashcards" element={<Flashcards />} />
          <Route path="/race" element={<Race />} />
          <Route path="/cheatsheet" element={<CheatSheet />} />
          <Route path="/patterns" element={<Patterns />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>

      <footer className="footer">
        DSA Study Lab · React, FastAPI, PostgreSQL &amp; Python in your browser
      </footer>

      {authOpen && <AuthModal />}
    </div>
  )
}

export default App
