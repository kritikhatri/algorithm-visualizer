import { useCallback, useEffect, useState } from 'react'
import { api } from '../api'
import { useAuth } from '../auth'
import { useApi } from '../useApi'

const BOX_LABELS = ['New', 'Box 1', 'Box 2', 'Box 3', 'Box 4', 'Mastered']

// Logged-in learners get a scheduled queue (due cards, then new ones) and their
// answers move cards between Leitner boxes. Guests can still flip through every card.
function FlashcardDeck({ topic, onReviewed }) {
  const { user, openAuth } = useAuth()
  const [reloadKey, setReloadKey] = useState(0)
  // reloadKey changes the URL so "check for more cards" refetches the queue.
  const params = new URLSearchParams({ ...(topic && { topic }), r: reloadKey })
  const { data, error } = useApi(`${user ? '/review' : '/flashcards'}?${params}`)

  if (error) return <p className="error-text">{error.message}</p>
  if (!data) return <p className="muted">Loading cards…</p>

  const cards = user ? [...data.due, ...data.new] : data.cards
  return (
    <Session
      key={`${topic}-${reloadKey}-${user?.id ?? 'guest'}`}
      initial={cards}
      stats={data.stats}
      scheduled={Boolean(user)}
      onLogin={openAuth}
      onRestart={() => setReloadKey((k) => k + 1)}
      onReviewed={onReviewed}
    />
  )
}

function Session({ initial, stats, scheduled, onLogin, onRestart, onReviewed }) {
  const [queue, setQueue] = useState(initial)
  const [flipped, setFlipped] = useState(false)
  const [tally, setTally] = useState({ right: 0, missed: 0 })
  const card = queue[0]

  const answer = useCallback(
    async (correct) => {
      if (!card || !flipped) return
      setTally((t) => ({ right: t.right + correct, missed: t.missed + !correct }))
      // Missed cards come back at the end of this session too.
      setQueue((q) => (correct ? q.slice(1) : [...q.slice(1), { ...q[0], box: 1 }]))
      setFlipped(false)
      if (scheduled) {
        await api(`/review/${card.id}`, { method: 'POST', body: { correct } }).catch(() => {})
        onReviewed?.()
      }
    },
    [card, flipped, scheduled, onReviewed]
  )

  useEffect(() => {
    function handleKey(event) {
      if (event.target.closest('input, select, textarea, .cm-editor')) return
      if (event.key === ' ' || event.key === 'Enter') {
        event.preventDefault()
        setFlipped((f) => !f)
      } else if (event.key === '1') {
        answer(false)
      } else if (event.key === '2') {
        answer(true)
      }
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [answer])

  const reviewed = tally.right + tally.missed

  return (
    <div className="deck">
      {scheduled && stats && (
        <div className="deck-stats">
          <span><strong>{stats.due}</strong> due today</span>
          <span><strong>{stats.seen}</strong> / {stats.total} learned</span>
          <span><strong>{stats.mastered}</strong> mastered</span>
          <div className="box-bar" aria-label="Cards per box">
            {stats.boxes.map((count, i) => (
              <span key={i} className={`box-${i + 1}`} style={{ flex: count || 0 }} title={`${BOX_LABELS[i + 1]}: ${count}`} />
            ))}
          </div>
        </div>
      )}

      {!scheduled && (
        <p className="deck-note">
          Practice mode. <button className="link" onClick={onLogin}>Log in</button> to schedule reviews so missed cards come back sooner.
        </p>
      )}

      {card ? (
        <>
          <button
            className={`flashcard ${flipped ? 'flipped' : ''}`}
            onClick={() => setFlipped(!flipped)}
            aria-label={flipped ? 'Show question' : 'Show answer'}
          >
            <span className="flashcard-inner">
              <span className="flashcard-face front">
                <span className="flashcard-tag">{card.box ? BOX_LABELS[card.box] : 'New'} · {card.topic}</span>
                <span className="flashcard-text">{card.front}</span>
                <span className="flashcard-hint">Click or press Space to reveal</span>
              </span>
              <span className="flashcard-face back">
                <span className="flashcard-tag">Answer</span>
                <span className="flashcard-text">{card.back}</span>
              </span>
            </span>
          </button>

          <div className="deck-actions">
            <button className="button ghost miss" onClick={() => answer(false)} disabled={!flipped}>
              ✗ Missed it <kbd>1</kbd>
            </button>
            <span className="muted">{queue.length} left</span>
            <button className="button primary" onClick={() => answer(true)} disabled={!flipped}>
              ✓ Got it <kbd>2</kbd>
            </button>
          </div>
        </>
      ) : (
        <div className="card deck-done">
          <h3>{reviewed ? 'Session complete! 🎉' : 'Nothing to review right now'}</h3>
          <p className="muted">
            {reviewed
              ? `You got ${tally.right} of ${reviewed} answers right${scheduled ? '. Missed cards will come back tomorrow; known ones are spaced further apart.' : '.'}`
              : 'All your cards are scheduled for later. Come back tomorrow, or pick another topic.'}
          </p>
          <button className="button ghost" onClick={onRestart}>↻ {scheduled ? 'Check for more cards' : 'Go again'}</button>
        </div>
      )}
    </div>
  )
}

export default FlashcardDeck
