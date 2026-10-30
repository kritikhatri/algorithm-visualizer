import { useEffect, useState } from 'react'

const MINUTES = [15, 25, 45]

function InterviewTimer() {
  const [minutes, setMinutes] = useState(25)
  const [left, setLeft] = useState(null)
  const running = left !== null && left > 0

  useEffect(() => {
    if (!running) return
    const timer = setTimeout(() => setLeft((s) => s - 1), 1000)
    return () => clearTimeout(timer)
  }, [running, left])

  if (left === null) {
    return (
      <span className="timer">
        <select aria-label="Timer length" value={minutes} onChange={(e) => setMinutes(Number(e.target.value))}>
          {MINUTES.map((m) => <option key={m} value={m}>{m} min</option>)}
        </select>
        <button className="button ghost small" onClick={() => setLeft(minutes * 60)}>⏱ Start</button>
      </span>
    )
  }

  const clock = `${String(Math.floor(left / 60)).padStart(2, '0')}:${String(left % 60).padStart(2, '0')}`
  return (
    <span className={`timer ${left < 60 ? 'urgent' : ''}`} role="timer">
      <strong>{left > 0 ? clock : "Time's up!"}</strong>
      <button className="button ghost small" onClick={() => setLeft(null)}>Stop</button>
    </span>
  )
}

export default InterviewTimer
