import { Link, NavLink, useParams } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../auth'
import { useApi } from '../useApi'
import CodeSnippet from '../components/CodeSnippet'
import Difficulty from '../components/Difficulty'
import Markdown from '../components/Markdown'
import Quiz from '../components/Quiz'
import { visualizers } from '../visualizers'
import NotFound from './NotFound'

const TABS = [
  { id: 'learn', label: 'Learn' },
  { id: 'visualize', label: 'Visualize' },
  { id: 'practice', label: 'Practice' },
  { id: 'quiz', label: 'Quiz' },
]

function Topic() {
  const { topicId, tab = 'learn' } = useParams()
  const { user, progress, openAuth, refreshProgress } = useAuth()
  const { data, error } = useApi(`/topics/${topicId}`)
  const { data: list } = useApi('/topics')

  if (error?.status === 404 || !TABS.some((t) => t.id === tab)) return <NotFound />
  if (error) return <p className="card error-text">{error.message}</p>
  if (!data) return <p className="muted">Loading…</p>

  const { topic } = data
  const Visualizer = visualizers[topic.visualizer]
  const isComplete = progress?.completedTopics.includes(topic.id)
  const solved = new Set(progress?.solvedProblems)

  const order = list?.topics ?? []
  const index = order.findIndex((t) => t.id === topic.id)
  const previous = order[index - 1]
  const next = order[index + 1]

  async function toggleComplete() {
    if (!user) {
      openAuth()
      return
    }
    await api(`/progress/topics/${topic.id}`, { method: isComplete ? 'DELETE' : 'PUT' })
    refreshProgress()
  }

  return (
    <article className="topic">
      <header className="topic-header">
        <div>
          <p className="eyebrow">
            {index >= 0 && `Topic ${index + 1} · `}{topic.category}
          </p>
          <h1>{topic.title}</h1>
          <p className="subtitle left">{topic.summary}</p>
        </div>
        <button className={`button ${isComplete ? 'success' : 'ghost'}`} onClick={toggleComplete}>
          {isComplete ? '✓ Completed' : 'Mark as complete'}
        </button>
      </header>

      <nav className="tabs page-tabs" aria-label="Topic sections">
        {TABS.map((t) => (
          <NavLink
            key={t.id}
            to={`/topics/${topic.id}${t.id === 'learn' ? '' : `/${t.id}`}`}
            end
            className={({ isActive }) => `tab ${isActive ? 'active' : ''}`}
          >
            {t.label}
          </NavLink>
        ))}
      </nav>

      {tab === 'learn' && (
        <div className="learn-layout">
          <section className="card">
            <Markdown source={topic.lesson} />
          </section>

          <aside className="learn-side">
            <section className="card">
              <h2 className="card-title">Complexity cheat sheet</h2>
              <table className="complexity-table">
                <thead>
                  <tr><th>Operation</th><th>Time</th><th>Space</th></tr>
                </thead>
                <tbody>
                  {topic.complexity.map((row) => (
                    <tr key={row.operation}>
                      <td>{row.operation}</td>
                      <td><code>{row.time}</code></td>
                      <td><code>{row.space}</code></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>

            <section className="card cta-card">
              <h2 className="card-title">Next steps</h2>
              <Link className="button ghost full" to={`/topics/${topic.id}/visualize`}>▶ Watch it run</Link>
              <Link className="button ghost full" to={`/topics/${topic.id}/practice`}>⌨ Practice problems</Link>
              <Link className="button ghost full" to={`/topics/${topic.id}/quiz`}>✓ Take the quiz</Link>
            </section>
          </aside>

          <section className="snippets">
            <h2 className="section-title">Python examples</h2>
            {topic.snippets.map((snippet) => (
              <CodeSnippet key={snippet.title} {...snippet} />
            ))}
          </section>
        </div>
      )}

      {tab === 'visualize' && (Visualizer ? <Visualizer key={topic.id} /> : <p>No visualizer yet.</p>)}

      {tab === 'practice' && (
        <section className="card">
          <ul className="problem-list">
            {topic.problems.map((problem) => (
              <li key={problem.id}>
                <Link to={`/problems/${problem.id}`} className="problem-row">
                  <span className={`status-icon ${solved.has(problem.id) ? 'solved' : ''}`}>
                    {solved.has(problem.id) ? '✓' : '○'}
                  </span>
                  <span className="problem-title">{problem.title}</span>
                  <Difficulty level={problem.difficulty} />
                  <span className="muted">Solve →</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      {tab === 'quiz' && <Quiz key={topic.id} topicId={topic.id} />}

      <nav className="pager" aria-label="Topics">
        {previous ? (
          <Link className="card pager-link" to={`/topics/${previous.id}`}>
            <span className="muted">← Previous</span>
            <strong>{previous.title}</strong>
          </Link>
        ) : <span />}
        {next && (
          <Link className="card pager-link next" to={`/topics/${next.id}`}>
            <span className="muted">Next →</span>
            <strong>{next.title}</strong>
          </Link>
        )}
      </nav>
    </article>
  )
}

export default Topic
