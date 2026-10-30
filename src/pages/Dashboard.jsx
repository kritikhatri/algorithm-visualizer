import { Link } from 'react-router-dom'
import { useAuth } from '../auth'
import { useApi } from '../useApi'

const WEAK_SCORE = 0.7

function earnedBadges(progress, topicCount, problemCount) {
  const solved = progress.solvedProblems.length
  const completed = progress.completedTopics.length
  const quizzes = Object.values(progress.quizBest)
  return [
    ['First solve', 'Solve a problem', solved >= 1],
    ['Problem solver', 'Solve 10 problems', solved >= 10],
    ['Half way', 'Solve half of all problems', solved >= problemCount / 2],
    ['First topic', 'Complete a topic', completed >= 1],
    ['Graduate', 'Complete every topic', completed === topicCount],
    ['Perfect score', 'Ace a quiz', quizzes.some((q) => q.score === q.total)],
    ['Week streak', 'Study 7 days in a row', progress.streak.longest >= 7],
  ]
}

function Dashboard() {
  const { user, progress, openAuth } = useAuth()
  const { data: topicData } = useApi('/topics')
  const { data: problemData } = useApi('/problems')
  const { data: review } = useApi(user ? '/review' : null)

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

  const solvedIn = (topicId) => problems.filter((p) => p.topic === topicId && solved.has(p.id)).length
  const totalIn = (topicId) => problems.filter((p) => p.topic === topicId).length
  const weakTopics = topics
    .filter((t) => {
      const best = progress.quizBest[t.id]
      return best && best.score / best.total < WEAK_SCORE
    })
    .map((t) => ({
      ...t,
      practice: problems.filter((p) => p.topic === t.id && !solved.has(p.id)).slice(0, 2),
    }))
  const badges = earnedBadges(progress, topics.length, problems.length)

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

        {review && (
          <section className="card review-card">
            <h2 className="card-title">Flashcards</h2>
            <p className="review-due"><strong>{review.stats.due}</strong> due today</p>
            <p className="muted">
              {review.stats.seen} of {review.stats.total} cards learned · {review.stats.mastered} mastered
            </p>
            <div className="box-bar" aria-hidden="true">
              {review.stats.boxes.map((count, i) => (
                <span key={i} className={`box-${i + 1}`} style={{ flex: count || 0 }} />
              ))}
            </div>
            <Link className="button primary small" to="/flashcards">
              {review.stats.due ? 'Review now' : 'Learn new cards'} →
            </Link>
          </section>
        )}

        <section className="card streak-card">
          <h2 className="card-title">Study streak</h2>
          <p className="review-due"><strong>{progress.streak.current}</strong> day{progress.streak.current === 1 ? '' : 's'}</p>
          <p className="muted">
            Longest: {progress.streak.longest} · {progress.streak.activeToday
              ? 'You studied today ✓'
              : 'Solve, quiz or review today to keep it going'}
          </p>
        </section>

        <section className="card badges-card">
          <h2 className="card-title">Badges</h2>
          <ul className="badges">
            {badges.map(([name, how, earned]) => (
              <li key={name} className={earned ? 'earned' : ''} title={how}>
                <strong>{earned ? '★' : '☆'} {name}</strong>
                <span className="muted">{how}</span>
              </li>
            ))}
          </ul>
        </section>

        {weakTopics.length > 0 && (
          <section className="card weak-card">
            <h2 className="card-title">Worth revisiting</h2>
            {weakTopics.map((t) => (
              <p key={t.id}>
                Your best quiz score on <Link to={`/topics/${t.id}`}>{t.title}</Link> is{' '}
                {progress.quizBest[t.id].score}/{progress.quizBest[t.id].total}.{' '}
                {t.practice.length > 0 && 'Try: '}
                {t.practice.map((p, i) => (
                  <span key={p.id}>{i > 0 && ', '}<Link to={`/problems/${p.id}`}>{p.title}</Link></span>
                ))}
              </p>
            ))}
          </section>
        )}

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
                    {solvedIn(topic.id)}/{totalIn(topic.id)} problems · {best ? `quiz ${Math.round((best.score / best.total) * 100)}%` : 'no quiz yet'}
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
