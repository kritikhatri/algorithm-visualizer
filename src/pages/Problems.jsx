import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth'
import { useApi } from '../useApi'
import Difficulty from '../components/Difficulty'

const LEVELS = ['All', 'Easy', 'Medium', 'Hard']

function Problems() {
  const { progress } = useAuth()
  const { data: problemData, error } = useApi('/problems')
  const { data: topicData } = useApi('/topics')
  const [query, setQuery] = useState('')
  const [topic, setTopic] = useState('all')
  const [level, setLevel] = useState('All')
  const [status, setStatus] = useState('all')

  const solved = new Set(progress?.solvedProblems)
  const attempted = new Set(progress?.attemptedProblems)
  const statusOf = (id) => (solved.has(id) ? 'solved' : attempted.has(id) ? 'attempted' : 'unsolved')
  const topicTitle = Object.fromEntries((topicData?.topics ?? []).map((t) => [t.id, t.title]))
  const problems = (problemData?.problems ?? []).filter(
    (problem) =>
      problem.title.toLowerCase().includes(query.trim().toLowerCase()) &&
      (topic === 'all' || problem.topic === topic) &&
      (level === 'All' || problem.difficulty === level) &&
      (status === 'all' || statusOf(problem.id) === status)
  )

  return (
    <>
      <header className="page-header">
        <p className="eyebrow">Practice</p>
        <h1>Problems</h1>
        <p className="subtitle left">
          Write Python, run it against test cases in your browser, and track what you've solved.
        </p>
      </header>

      <div className="filters">
        <input
          type="search"
          aria-label="Search problems"
          placeholder="Search problems…"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
        <select aria-label="Topic" value={topic} onChange={(event) => setTopic(event.target.value)}>
          <option value="all">All topics</option>
          {(topicData?.topics ?? []).map((t) => (
            <option key={t.id} value={t.id}>{t.title}</option>
          ))}
        </select>
        <div className="tabs compact" role="group" aria-label="Difficulty">
          {LEVELS.map((name) => (
            <button
              key={name}
              className={`tab ${level === name ? 'active' : ''}`}
              aria-pressed={level === name}
              onClick={() => setLevel(name)}
            >
              {name}
            </button>
          ))}
        </div>
        {progress && (
          <select aria-label="Status" value={status} onChange={(event) => setStatus(event.target.value)}>
            <option value="all">Any status</option>
            <option value="solved">Solved</option>
            <option value="attempted">Attempted</option>
            <option value="unsolved">Unsolved</option>
          </select>
        )}
      </div>

      {error && <p className="card error-text">{error.message}</p>}

      <section className="card">
        {problems.length === 0 && problemData ? (
          <p className="muted">No problems match these filters.</p>
        ) : (
          <ul className="problem-list">
            {problems.map((problem) => (
              <li key={problem.id}>
                <Link to={`/problems/${problem.id}`} className="problem-row">
                  <span className={`status-icon ${solved.has(problem.id) ? 'solved' : ''}`}>
                    {solved.has(problem.id) ? '✓' : '○'}
                  </span>
                  <span className="problem-title">{problem.title}</span>
                  <span className="muted problem-topic">{topicTitle[problem.topic]}</span>
                  <Difficulty level={problem.difficulty} />
                </Link>
              </li>
            ))}
          </ul>
        )}
      </section>
    </>
  )
}

export default Problems
