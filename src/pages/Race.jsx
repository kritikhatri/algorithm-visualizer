import { useEffect, useMemo, useState } from 'react'
import { ArrayBars, NumberListInput } from '../visualizers/common'
import { randomInts } from '../visualizers/helpers'
import { sortingAlgorithms } from '../visualizers/sortingSteps'

function Lane({ id, onChange, frames, step }) {
  const frame = frames[Math.min(step, frames.length - 1)]
  const finished = step >= frames.length - 1
  return (
    <section className="card race-lane">
      <select aria-label="Algorithm" value={id} onChange={(event) => onChange(event.target.value)}>
        {Object.entries(sortingAlgorithms).map(([key, { name }]) => (
          <option key={key} value={key}>{name} Sort</option>
        ))}
      </select>
      <ArrayBars frame={frame} />
      <div className="stat-chips">
        <span>Comparisons <strong>{frame.comparisons}</strong></span>
        <span>Swaps / writes <strong>{frame.swaps}</strong></span>
        <span>Steps <strong>{Math.min(step + 1, frames.length)} / {frames.length}</strong></span>
        {finished && <span className="done-badge">✓ Finished</span>}
      </div>
    </section>
  )
}

function Race() {
  const [values, setValues] = useState(() => randomInts(10, 5, 99))
  const [left, setLeft] = useState('bubble')
  const [right, setRight] = useState('merge')
  const [step, setStep] = useState(0)
  const [running, setRunning] = useState(false)

  const leftFrames = useMemo(() => sortingAlgorithms[left].steps(values), [left, values])
  const rightFrames = useMemo(() => sortingAlgorithms[right].steps(values), [right, values])
  const longest = Math.max(leftFrames.length, rightFrames.length)
  const active = running && step < longest - 1

  useEffect(() => {
    if (!active) return
    const timer = setTimeout(() => setStep((s) => s + 1), 120)
    return () => clearTimeout(timer)
  }, [active, step])

  function restart(change) {
    change?.()
    setStep(0)
    setRunning(false)
  }

  let verdict = 'Same input, one step per tick. Which finishes first?'
  if (step >= Math.min(leftFrames.length, rightFrames.length) - 1 && step > 0) {
    verdict = leftFrames.length === rightFrames.length
      ? 'A tie on steps!'
      : `${sortingAlgorithms[leftFrames.length < rightFrames.length ? left : right].name} Sort finished first.`
  }

  return (
    <>
      <header className="page-header">
        <p className="eyebrow">Race mode</p>
        <h1>Sorting race</h1>
        <p className="subtitle left">{verdict}</p>
      </header>
      <div className="filters">
        <button className="button primary" onClick={() => (step >= longest - 1 ? (setStep(0), setRunning(true)) : setRunning(!running))}>
          {step >= longest - 1 ? '↻ Race again' : active ? 'Ⅱ Pause' : '▶ Start race'}
        </button>
        <NumberListInput initial={values} onSubmit={(next) => restart(() => setValues(next))} maxLength={12} min={1} max={99} />
      </div>
      <div className="race">
        <Lane id={left} onChange={(id) => restart(() => setLeft(id))} frames={leftFrames} step={step} />
        <Lane id={right} onChange={(id) => restart(() => setRight(id))} frames={rightFrames} step={step} />
      </div>
    </>
  )
}

export default Race
