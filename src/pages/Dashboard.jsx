import { Link } from 'react-router-dom'
import { useAuth } from '../auth'
import { useApi } from '../useApi'

function Dashboard() {
  const { user, progress, openAuth } = useAuth()
  const { data: topicData } = useApi('/topics')
  const { data: problemData } = useApi('/problems')

  if (!user) {
    return (
      <section className="card empty-state">
        <h1>Your progress</h1>
        <p className="muted">Log in to track completed topics, solved problems and quiz scores.</p>
        <button className="button primary" onClick={openAuth}>Log in or sign up</button>
      </section>
    )
  }

  if (!progress || !topicData || !problemData) return <p className="muted">Loading…</p>

  const topics = topicData.topics
  const problems = problemData.problems
  const completed = new Set(progress.completedTopics)
  const solved = new Set(progress.solvedProblems)
  const topicTitle = Object.fromEntries(topics.map((t) => [t.id, t.title]))
  const problemTitle = Object.fromEntries(problems.map((p) => [p.id, p.title]))
  const nextTopic = topics.find((t) => !completed.has(t.id))

  const byDifficulty = ['Easy', 'Medium', 'Hard'].map((level) => {
    const all = problems.filter((p) => p.difficulty === level)
    return { level, total: all.length, solved: all.filter((p) => solved.has(p.id)).length }
  })

  const percent = Math.round(
    ((completed.size + solved.size) / (topics.length + problems.length)) * 100
  )

  return (
    <>
      <header className="page-header">
        <p className="eyebrow">Welcome back, {user.username}</p>
        <h1>Your progress</h1>
      </header>

      <div className="dash-grid">
        <section className="card overall">
          <div className="ring" style={{ '--value': percent }} role="img" aria-label={`${percent}% complete`}>
            <span>{percent}%</span>
          </div>
          <div>
            <h2 className="card-title">Overall</h2>
            <p className="muted">{completed.size} / {topics.length} topics completed</p>
            <p className="muted">{solved.size} / {problems.length} problems solved</p>
            {nextTopic && (
              <Link className="button primary small" to={`/topics/${nextTopic.id}`}>
                Up next: {nextTopic.title} →
              </Link>
            )}
          </div>
        </section>

        <section className="card">
          <h2 className="card-title">Problems by difficulty</h2>
          {byDifficulty.map(({ level, total, solved: count }) => (
            <div className="meter" key={level}>
              <span className={`difficulty ${level.toLowerCase()}`}>{level}</span>
              <div className="progress-bar"><span style={{ width: `${total ? (count / total) * 100 : 0}%` }} /></div>
              <span className="meter-value">{count} / {total}</span>
            </div>
          ))}
        </section>

        <section className="card topics-progress">
          <h2 className="card-title">Topics</h2>
          <ul className="topic-checklist">
            {topics.map((topic) => {
              const best = progress.quizBest[topic.id]
              return (
                <li key={topic.id}>
                  <span className={`status-icon ${completed.has(topic.id) ? 'solved' : ''}`}>
                    {completed.has(topic.id) ? '✓' : '○'}
                  </span>
                  <Link to={`/topics/${topic.id}`}>{topic.title}</Link>
                  <span className="muted">
                    {best ? `Quiz best ${best.score}/${best.total}` : 'Quiz not taken'}
                  </span>
                </li>
              )
            })}
          </ul>
        </section>

        <section className="card">
          <h2 className="card-title">Recently solved</h2>
          {progress.recentlySolved.length ? (
            <ul className="activity">
              {progress.recentlySolved.map((item) => (
                <li key={item.problem}>
                  <Link to={`/problems/${item.problem}`}>{problemTitle[item.problem] ?? item.problem}</Link>
                  <time className="muted" dateTime={item.solvedAt}>
                    {new Date(item.solvedAt).toLocaleDateString(undefined, { month: 'short', day: 'numeric' })}
                  </time>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">Nothing yet. <Link to="/problems">Pick a problem</Link> to start.</p>
          )}

          <h2 className="card-title spaced">Recent quizzes</h2>
          {progress.recentQuizzes.length ? (
            <ul className="activity">
              {progress.recentQuizzes.map((quiz, i) => (
                <li key={i}>
                  <Link to={`/topics/${quiz.topic}/quiz`}>{topicTitle[quiz.topic] ?? quiz.topic}</Link>
                  <span className="muted">{quiz.score} / {quiz.total}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">No quiz attempts yet.</p>
          )}
        </section>
      </div>
    </>
  )
}

export default Dashboard
