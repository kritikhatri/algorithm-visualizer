import { Link } from 'react-router-dom'
import { useAuth } from '../auth'
import { useApi } from '../useApi'
import Difficulty from '../components/Difficulty'
import HeroDemo from '../components/HeroDemo'

// One wine family, rosé through champagne: each category gets one shade.
const CATEGORY_ACCENT = {
  Foundations: '#f4c27a',
  'Linear Structures': '#ff6b8b',
  Techniques: '#f28fad',
  Algorithms: '#ef476f',
  'Trees & Graphs': '#e9a0a0',
}

const TOPIC_ICON = {
  'big-o': 'O(n)',
  'bit-manipulation': '01',
  arrays: '[ ]',
  'sliding-window': '[→]',
  hashing: '#',
  'linked-lists': '→',
  'stacks-queues': '≡',
  recursion: 'f()',
  sorting: '↑↓',
  'binary-search': '½',
  trees: '⋔',
  tries: 'abc',
  heaps: '△',
  graphs: '◇',
  'shortest-paths': '⇢',
  'union-find': '∪',
  greedy: '★',
  'dynamic-programming': 'dp',
}

const STEPS = [
  ['1', 'Learn', 'Short lessons with runnable Python examples.'],
  ['2', 'Watch', 'Step through animations as each line of code runs.'],
  ['3', 'Practice', 'Solve problems and run tests right in your browser.'],
  ['4', 'Remember', 'Quizzes and spaced flashcards make it stick.'],
]

function Home() {
  const { user, progress, openAuth } = useAuth()
  const { data, error } = useApi('/topics')
  const { data: daily } = useApi('/daily')
  const { data: problemData } = useApi(progress?.attemptedProblems.length ? '/problems' : null)

  const topics = data?.topics ?? []
  const completed = new Set(progress?.completedTopics)
  const solved = new Set(progress?.solvedProblems)
  const totalProblems = topics.reduce((sum, topic) => sum + topic.problemCount, 0)
  const totalQuestions = topics.reduce((sum, topic) => sum + topic.quizCount, 0)
  const nextTopic = topics.find((topic) => !completed.has(topic.id)) ?? topics[0]

  const resumeProblem = problemData?.problems.find((p) => p.id === progress?.attemptedProblems[0])

  return (
    <>
      <section className="hero hero-split">
        <div className="hero-copy">
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
        </div>
        <HeroDemo />
      </section>

      <section className="steps" aria-label="How it works">
        {STEPS.map(([icon, title, text]) => (
          <article className="step" key={title}>
            <span className="step-icon" aria-hidden="true">{icon}</span>
            <h3>{title}</h3>
            <p className="muted">{text}</p>
          </article>
        ))}
      </section>

      {daily && (
        <section className="card daily-card">
          <div>
            <p className="eyebrow">Today's problem</p>
            <h2>{daily.problem.title}</h2>
          </div>
          <div className="toolbar-actions">
            <Difficulty level={daily.problem.difficulty} />
            {solved.has(daily.problem.id) && <span className="done-badge">✓ Solved</span>}
            <Link className="button ghost" to={`/problems/${daily.problem.id}`}>Solve it →</Link>
            <Link className="button ghost" to="/patterns">Pattern quiz</Link>
          </div>
        </section>
      )}

      {user && progress && nextTopic && (
        <section className="card continue-card">
          <div>
            <p className="eyebrow">Continue where you left off</p>
            <h2>{nextTopic.title}</h2>
            <p className="muted">{nextTopic.summary}</p>
          </div>
          <div className="toolbar-actions">
            {resumeProblem && (
              <Link className="button ghost" to={`/problems/${resumeProblem.id}`}>Resume: {resumeProblem.title}</Link>
            )}
            <Link className="button primary" to={`/topics/${nextTopic.id}`}>Continue →</Link>
          </div>
        </section>
      )}

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
          {topics.map((topic, index) => {
            const icon = TOPIC_ICON[topic.id] ?? '•'
            const accent = CATEGORY_ACCENT[topic.category] ?? '#ef476f'
            return (
            <Link
              className="card topic-card"
              to={`/topics/${topic.id}`}
              key={topic.id}
              style={{ '--accent': accent, animationDelay: `${index * 35}ms` }}
            >
              <span className="topic-icon" aria-hidden="true">{icon}</span>
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
            )
          })}
        </div>
      </section>
    </>
  )
}

export default Home
