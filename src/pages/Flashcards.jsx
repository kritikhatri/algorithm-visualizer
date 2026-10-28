import { useSearchParams } from 'react-router-dom'
import { useApi } from '../useApi'
import FlashcardDeck from '../components/FlashcardDeck'

function Flashcards() {
  const [params, setParams] = useSearchParams()
  const topic = params.get('topic') ?? ''
  const { data } = useApi('/topics')

  return (
    <>
      <header className="page-header">
        <p className="eyebrow">Spaced review</p>
        <h1>Flashcards</h1>
        <p className="subtitle left">
          Recall beats re-reading. Cards you miss come back tomorrow; cards you know are spaced
          further apart (1, 2, 4, 8, then 16 days).
        </p>
      </header>

      <div className="filters">
        <select
          aria-label="Topic"
          value={topic}
          onChange={(event) => setParams(event.target.value ? { topic: event.target.value } : {})}
        >
          <option value="">All topics</option>
          {(data?.topics ?? []).map((t) => (
            <option key={t.id} value={t.id}>{t.title}</option>
          ))}
        </select>
        <span className="muted small-note">Shortcuts: <kbd>Space</kbd> flip · <kbd>1</kbd> missed · <kbd>2</kbd> got it</span>
      </div>

      <FlashcardDeck key={topic} topic={topic || null} />
    </>
  )
}

export default Flashcards
