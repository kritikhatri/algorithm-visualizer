import { useState } from 'react'
import { api } from '../api'
import { useAuth } from '../auth'
import { useApi } from '../useApi'

function Quiz({ topicId }) {
  const { user, openAuth, refreshProgress } = useAuth()
  const { data, error } = useApi(`/topics/${topicId}/quiz`)
  const [answers, setAnswers] = useState({})
  const [result, setResult] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  if (error) return <p className="error-text">{error.message}</p>
  if (!data) return <p className="muted">Loading quiz…</p>

  const { questions } = data
  const answeredAll = questions.every((_, i) => answers[i] !== undefined)

  async function handleSubmit() {
    setSubmitting(true)
    try {
      const response = await api(`/topics/${topicId}/quiz`, {
        method: 'POST',
        body: { answers: questions.map((_, i) => answers[i] ?? null) },
      })
      setResult(response)
      if (user) refreshProgress()
    } finally {
      setSubmitting(false)
    }
  }

  function handleRetry() {
    setAnswers({})
    setResult(null)
  }

  return (
    <div className="quiz">
      {result && (
        <div className={`quiz-score ${result.score === result.total ? 'perfect' : ''}`}>
          <strong>{result.score} / {result.total}</strong>
          <span>
            {result.score === result.total
              ? 'Perfect score! 🎉'
              : 'Review the explanations below, then try again.'}
          </span>
          {!user && (
            <button className="link" onClick={openAuth}>Log in to save your scores</button>
          )}
        </div>
      )}

      {questions.map((question, qi) => {
        const outcome = result?.results[qi]
        return (
          <fieldset className="question" key={qi} disabled={!!result}>
            <legend>
              <span className="question-number">{qi + 1}</span>
              {question.question}
            </legend>
            <div className="options">
              {question.options.map((option, oi) => {
                const state = !outcome
                  ? answers[qi] === oi ? 'selected' : ''
                  : oi === outcome.answer
                    ? 'correct'
                    : answers[qi] === oi
                      ? 'wrong'
                      : ''
                return (
                  <label className={`option ${state}`} key={oi}>
                    <input
                      type="radio"
                      name={`q${qi}`}
                      checked={answers[qi] === oi}
                      onChange={() => setAnswers({ ...answers, [qi]: oi })}
                    />
                    <span>{option}</span>
                  </label>
                )
              })}
            </div>
            {outcome && (
              <p className={`explanation ${outcome.correct ? 'good' : 'bad'}`}>
                {outcome.correct ? '✓ Correct. ' : '✗ Not quite. '}
                {outcome.explanation}
              </p>
            )}
          </fieldset>
        )
      })}

      <div className="quiz-actions">
        {result ? (
          <button className="button primary" onClick={handleRetry}>↻ Try again</button>
        ) : (
          <button
            className="button primary"
            onClick={handleSubmit}
            disabled={!answeredAll || submitting}
          >
            {submitting ? 'Checking…' : 'Submit answers'}
          </button>
        )}
      </div>
    </div>
  )
}

export default Quiz
