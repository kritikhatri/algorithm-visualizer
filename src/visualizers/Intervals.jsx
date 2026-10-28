import { useMemo, useState } from 'react'
import { PlayerControls, VizLayout } from './common'
import { raw, useStepPlayer } from './helpers'

const CODE = `def max_meetings(intervals):
    count, end = 0, float("-inf")
    for start, finish in sorted(intervals, key=lambda iv: iv[1]):
        if start >= end:
            count += 1
            end = finish
    return count`

const PRESETS = {
  'Workday meetings': [[1, 4], [3, 5], [0, 6], [5, 7], [3, 9], [5, 9], [6, 10], [8, 11], [8, 12], [2, 14], [12, 16]],
  'Long meeting trap': [[0, 12], [1, 3], [4, 6], [7, 9], [10, 12]],
}

function greedySteps(intervals) {
  const order = intervals
    .map((iv, i) => ({ id: i, start: iv[0], end: iv[1] }))
    .sort((a, b) => a.end - b.end || a.start - b.start)
  const frames = []
  const kept = []
  const skipped = []
  let end = -Infinity

  const push = (line, message, extra = {}) =>
    frames.push({ order, kept: [...kept], skipped: [...skipped], end, line, message, ...extra })

  push(3, 'Sort the meetings by finishing time. Finishing early leaves the most room for the rest.')
  for (const iv of order) {
    push(4, `[${iv.start}, ${iv.end}]: does it start at or after ${Number.isFinite(end) ? end : '−∞'}?`, { current: iv.id })
    if (iv.start >= end) {
      kept.push(iv.id)
      end = iv.end
      push(6, `Yes, keep it. The room is now busy until ${end}.`, { current: iv.id })
    } else {
      skipped.push(iv.id)
      push(4, `No, it overlaps the last kept meeting. Skip it.`, { current: iv.id })
    }
  }
  push(7, `Greedy keeps ${kept.length} meeting(s), the maximum possible.`)
  return frames
}

function Intervals() {
  const [preset, setPreset] = useState('Workday meetings')
  const intervals = PRESETS[preset]
  const frames = useMemo(() => greedySteps(intervals), [intervals])
  const player = useStepPlayer(frames)
  const { frame } = player

  const max = Math.max(...intervals.map(([, e]) => e))
  const rowOf = Object.fromEntries(frame.order.map((iv, i) => [iv.id, i]))

  return (
    <VizLayout
      toolbar={
        <div className="tabs compact" role="group" aria-label="Example">
          {Object.keys(PRESETS).map((name) => (
            <button key={name} className={`tab ${preset === name ? 'active' : ''}`} aria-pressed={preset === name} onClick={() => setPreset(name)}>
              {name}
            </button>
          ))}
        </div>
      }
      visual={
        <div className="timeline">
          <div className="timeline-axis">
            {Array.from({ length: max + 1 }, (_, t) => (
              <span key={t} style={{ left: `${(t / max) * 100}%` }}>{t}</span>
            ))}
          </div>
          {Number.isFinite(frame.end) && (
            <div className="timeline-end" style={{ left: `calc(8px + (100% - 16px) * ${frame.end / max})` }} />
          )}
          {frame.order.map((iv) => {
            const state = frame.current === iv.id
              ? 'comparing'
              : frame.kept.includes(iv.id)
                ? 'sorted'
                : frame.skipped.includes(iv.id) ? 'dim' : ''
            return (
              <div className="timeline-row" key={iv.id} style={{ order: rowOf[iv.id] }}>
                <div
                  className={`interval ${state}`}
                  style={{ left: `${(iv.start / max) * 100}%`, width: `${((iv.end - iv.start) / max) * 100}%` }}
                >
                  {iv.start}–{iv.end}
                </div>
              </div>
            )
          })}
        </div>
      }
      legend={[['comparing', 'Considering'], ['sorted', 'Kept'], ['dim', 'Skipped (overlaps)']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={{ count: frame.kept.length, end: Number.isFinite(frame.end) ? frame.end : raw('float("-inf")') }}
    />
  )
}

export default Intervals
