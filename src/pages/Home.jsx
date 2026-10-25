import { Link } from 'react-router-dom'
import { useAuth } from '../auth'
import { useApi } from '../useApi'

function Home() {
  const { user, progress, openAuth } = useAuth()
  const { data, error } = useApi('/topics')

  const topics = data?.topics ?? []
  const completed = new Set(progress?.completedTopics)
  const solved = new Set(progress?.solvedProblems)
  const totalProblems = topics.reduce((sum, topic) => sum + topic.problemCount, 0)
  const totalQuestions = topics.reduce((sum, topic) => sum + topic.quizCount, 0)
  const nextTopic = topics.find((topic) => !completed.has(topic.id)) ?? topics[0]

  return (
    <>
      <section className="hero">
        <p className="eyebrow">Data structures & algorithms in Python</p>
        <h1>
          Learn DSA by <span className="gradient-text">seeing it run</span>
        </h1>
        <p className="subtitle">
          Short lessons, step-by-step visualizers that highlight each line of Python,
          practice problems you solve right in the browser, and quizzes to lock it in.
        </p>
        <div className="hero-actions">
          {nextTopic && (
            <Link className="button primary" to={`/topics/${nextTopic.id}`}>
              {completed.size ? `Continue: ${nextTopic.title}` : 'Start learning'} →
            </Link>
          )}
          <Link className="button ghost" to="/playground">Open Python playground</Link>
        </div>

        <dl className="hero-stats">
          <div><dt>Topics</dt><dd>{topics.length || '—'}</dd></div>
          <div><dt>Practice problems</dt><dd>{totalProblems || '—'}</dd></div>
          <div><dt>Quiz questions</dt><dd>{totalQuestions || '—'}</dd></div>
        </dl>
      </section>

      {user && progress && topics.length > 0 && (
        <section className="card progress-strip">
          <div>
            <p className="eyebrow">Your progress</p>
            <strong>{completed.size} of {topics.length} topics · {solved.size} of {totalProblems} problems solved</strong>
          </div>
          <div className="progress-bar" aria-hidden="true">
            <span style={{ width: `${(completed.size / topics.length) * 100}%` }} />
          </div>
          <Link className="button ghost small" to="/dashboard">View dashboard</Link>
        </section>
      )}

      {!user && (
        <section className="card progress-strip">
          <p>
            <strong>Track your journey.</strong>{' '}
            <span className="muted">Create a free account to save solutions, quiz scores and completed topics.</span>
          </p>
          <button className="button primary small" onClick={openAuth}>Sign up</button>
        </section>
      )}

      {error && (
        <p className="card error-text">
          Couldn't load topics ({error.message}). Is the API running on port 8000?
        </p>
      )}

      <section className="topic-group">
        <h2 className="section-title">Learning path</h2>
        <div className="topic-grid">
          {topics.map((topic, index) => (
            <Link className="card topic-card" to={`/topics/${topic.id}`} key={topic.id}>
              <span className="topic-number">
                {String(index + 1).padStart(2, '0')} · {topic.category}
              </span>
              {completed.has(topic.id) && <span className="done-badge">✓ Done</span>}
              <h3>{topic.title}</h3>
              <p className="muted">{topic.summary}</p>
              <span className="topic-meta">
                {topic.problemCount} problems · {topic.quizCount}-question quiz
              </span>
            </Link>
          ))}
        </div>
      </section>
    </>
  )
}

export default Home
