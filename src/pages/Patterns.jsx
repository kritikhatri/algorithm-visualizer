import { useState } from 'react'
import { useApi } from '../useApi'

function Patterns() {
  const { data, error } = useApi('/patterns')
  const [index, setIndex] = useState(0)
  const [choice, setChoice] = useState(null)
  const [score, setScore] = useState(0)

  if (error) return <p className="card error-text">{error.message}</p>
  if (!data) return <p className="muted">Loading…</p>

  const { questions, techniques } = data
  const finished = index >= questions.length

  function restart() {
    setIndex(0)
    setChoice(null)
    setScore(0)
  }

  function pick(option) {
    if (choice) return
    setChoice(option)
    if (option === questions[index].answer) setScore(score + 1)
  }

  const question = questions[index]

  return (
    <div className="quiz patterns">
      <header className="page-header">
        <p className="eyebrow">Pattern recognition</p>
        <h1>Which technique fits?</h1>
        <p className="subtitle left">Spotting the pattern is half of solving the problem.</p>
      </header>

      {finished ? (
        <div className="quiz-score">
          <strong>{score} / {questions.length}</strong>
          <button className="button primary" onClick={restart}>↻ Try again</button>
        </div>
      ) : (
        <section className="question">
          <p className="muted small-note">Question {index + 1} of {questions.length} · Score {score}</p>
          <h2 className="pattern-question">{question.question}</h2>
          <div className="pattern-options">
            {techniques.map((option) => (
              <button
                key={option}
                className={`option ${choice && option === question.answer ? 'correct' : choice === option ? 'wrong' : ''}`}
                onClick={() => pick(option)}
              >
                {option}
              </button>
            ))}
          </div>
          {choice && (
            <>
              <p className={`explanation ${choice === question.answer ? 'good' : 'bad'}`}>
                {choice === question.answer ? '✓ Correct. ' : `✗ It's ${question.answer}. `}
                {question.why}
              </p>
              <div className="quiz-actions">
                <button className="button primary" onClick={() => { setIndex(index + 1); setChoice(null) }}>Next →</button>
              </div>
            </>
          )}
        </section>
      )}
    </div>
  )
}

export default Patterns
