import { useState } from 'react'
import { VizLayout } from './common'

const CODE = `import math

def operations(n):
    return {
        "O(1)": 1,
        "O(log n)": math.log2(n),
        "O(n)": n,
        "O(n log n)": n * math.log2(n),
        "O(n²)": n ** 2,
        "O(2ⁿ)": 2 ** n,
    }`

// Fixed categorical order; colors come from --series-1..6 in CSS.
const SERIES = [
  { id: 'O(1)', fn: () => 1, line: 5 },
  { id: 'O(log n)', fn: (n) => Math.log2(n), line: 6 },
  { id: 'O(n)', fn: (n) => n, line: 7 },
  { id: 'O(n log n)', fn: (n) => n * Math.log2(n), line: 8 },
  { id: 'O(n²)', fn: (n) => n * n, line: 9 },
  { id: 'O(2ⁿ)', fn: (n) => 2 ** n, line: 10 },
]

const W = 640
const H = 320
const M = { top: 16, right: 84, bottom: 36, left: 56 }
const PLOT_W = W - M.left - M.right
const PLOT_H = H - M.top - M.bottom

function format(value) {
  if (value >= 1e9) return value.toExponential(1).replace('e+', 'e')
  if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`
  if (value >= 1e4) return `${Math.round(value / 1e3)}k`
  return Number.isInteger(value) ? String(value) : value.toFixed(1)
}

function duration(ops) {
  const seconds = ops / 1e6 // 1 operation per microsecond
  if (seconds < 1e-3) return `${(seconds * 1e6).toFixed(0)} µs`
  if (seconds < 1) return `${(seconds * 1e3).toFixed(1)} ms`
  if (seconds < 120) return `${seconds.toFixed(1)} s`
  if (seconds < 7200) return `${(seconds / 60).toFixed(0)} min`
  if (seconds < 172800) return `${(seconds / 3600).toFixed(0)} hours`
  const years = seconds / 31557600
  return years < 1 ? `${(seconds / 86400).toFixed(0)} days` : `${format(years)} years`
}

// Direct labels at each line's right end, nudged apart so they never overlap.
function endLabels(series, maxN, limit, y) {
  const GAP = 14
  const labels = series
    .map((s, i) => ({ s, i, value: s.fn(maxN) }))
    .filter(({ value }) => value <= limit)
    .map((label) => ({ ...label, labelY: y(label.value) }))
    .sort((a, b) => b.labelY - a.labelY)
  for (let k = 1; k < labels.length; k++) {
    labels[k].labelY = Math.min(labels[k].labelY, labels[k - 1].labelY - GAP)
  }
  return labels
}

function Growth() {
  const [maxN, setMaxN] = useState(16)
  const [logScale, setLogScale] = useState(false)
  const [hoverN, setHoverN] = useState(null)
  const [focus, setFocus] = useState(null)
  const [tableN, setTableN] = useState(1000)

  const ns = Array.from({ length: maxN }, (_, i) => i + 1)
  const yMax = logScale ? 2 ** maxN : maxN * maxN * 1.15
  const x = (n) => M.left + ((n - 1) / (maxN - 1)) * PLOT_W
  const y = (v) =>
    logScale
      ? M.top + PLOT_H - (Math.log10(Math.max(v, 1)) / Math.log10(yMax)) * PLOT_H
      : M.top + PLOT_H - (Math.min(v, yMax) / yMax) * PLOT_H

  const ticks = logScale
    ? Array.from({ length: Math.floor(Math.log10(yMax)) + 1 }, (_, i) => 10 ** i)
    : Array.from({ length: 5 }, (_, i) => Math.round((yMax / 4) * i))

  function handleMove(event) {
    const rect = event.currentTarget.getBoundingClientRect()
    const px = ((event.clientX - rect.left) / rect.width) * W
    const n = Math.round(((px - M.left) / PLOT_W) * (maxN - 1)) + 1
    setHoverN(n >= 1 && n <= maxN ? n : null)
  }

  const focused = SERIES.find((s) => s.id === focus)

  return (
    <VizLayout
      toolbar={
        <>
          <label className="inline-field">
            <span>n up to</span>
            <input type="range" min="5" max="30" value={maxN} onChange={(event) => setMaxN(Number(event.target.value))} />
            <strong>{maxN}</strong>
          </label>
          <div className="tabs compact" role="group" aria-label="Y-axis scale">
            {[[false, 'Linear'], [true, 'Log scale']].map(([value, label]) => (
              <button key={label} className={`tab ${logScale === value ? 'active' : ''}`} aria-pressed={logScale === value} onClick={() => setLogScale(value)}>
                {label}
              </button>
            ))}
          </div>
        </>
      }
      visual={
        <div className="growth">
          <div className="chart-legend" role="list">
            {SERIES.map((s, i) => (
              <button
                key={s.id}
                role="listitem"
                className={`legend-key ${focus && focus !== s.id ? 'faded' : ''}`}
                onMouseEnter={() => setFocus(s.id)}
                onMouseLeave={() => setFocus(null)}
                onFocus={() => setFocus(s.id)}
                onBlur={() => setFocus(null)}
              >
                <i style={{ background: `var(--series-${i + 1})` }} /> {s.id}
              </button>
            ))}
          </div>

          <div className="chart-box">
            <svg
              viewBox={`0 0 ${W} ${H}`}
              className="chart"
              role="img"
              aria-label={`Operations versus input size n for six complexity classes, n from 1 to ${maxN}`}
              onMouseMove={handleMove}
              onMouseLeave={() => setHoverN(null)}
            >
              <defs>
                <clipPath id="plot-clip">
                  <rect x={M.left} y={M.top - 2} width={PLOT_W + 2} height={PLOT_H + 4} />
                </clipPath>
              </defs>

              {ticks.map((t) => (
                <g key={t}>
                  <line className="grid-line" x1={M.left} x2={M.left + PLOT_W} y1={y(t)} y2={y(t)} />
                  <text className="axis-label" x={M.left - 8} y={y(t)} textAnchor="end" dy="0.32em">{format(t)}</text>
                </g>
              ))}
              {ns.filter((n) => n === 1 || n % 5 === 0).map((n) => (
                <text key={n} className="axis-label" x={x(n)} y={H - M.bottom + 18} textAnchor="middle">{n}</text>
              ))}
              <text className="axis-title" x={M.left + PLOT_W / 2} y={H - 4} textAnchor="middle">input size n</text>
              <line className="axis-line" x1={M.left} x2={M.left + PLOT_W} y1={M.top + PLOT_H} y2={M.top + PLOT_H} />

              <g clipPath="url(#plot-clip)">
                {SERIES.map((s, i) => (
                  <polyline
                    key={s.id}
                    className={`series-line ${focus && focus !== s.id ? 'faded' : ''}`}
                    style={{ stroke: `var(--series-${i + 1})` }}
                    points={ns.map((n) => `${x(n)},${y(s.fn(n))}`).join(' ')}
                  />
                ))}
              </g>

              {endLabels(SERIES, maxN, logScale ? Infinity : yMax, y).map(({ s, i, labelY }) => (
                <text
                  key={s.id}
                  className={`end-label ${focus && focus !== s.id ? 'faded' : ''}`}
                  x={M.left + PLOT_W + 6}
                  y={labelY}
                  dy="0.32em"
                >
                  <tspan style={{ fill: `var(--series-${i + 1})` }}>●</tspan> {s.id}
                </text>
              ))}

              {hoverN && (
                <g className="crosshair">
                  <line x1={x(hoverN)} x2={x(hoverN)} y1={M.top} y2={M.top + PLOT_H} />
                  {SERIES.map((s, i) =>
                    logScale || s.fn(hoverN) <= yMax ? (
                      <circle key={s.id} cx={x(hoverN)} cy={y(s.fn(hoverN))} r="4.5" style={{ fill: `var(--series-${i + 1})` }} />
                    ) : null
                  )}
                </g>
              )}
            </svg>

            {hoverN && (
              <div
                className="chart-tooltip"
                style={{ left: `${(x(hoverN) / W) * 100}%` }}
              >
                <strong>n = {hoverN}</strong>
                {SERIES.map((s, i) => (
                  <span key={s.id}>
                    <i style={{ background: `var(--series-${i + 1})` }} />
                    {s.id}<b>{format(s.fn(hoverN))}</b>
                  </span>
                ))}
              </div>
            )}
          </div>

          <div className="growth-table">
            <label className="inline-field">
              <span>Operations when n =</span>
              <select value={tableN} onChange={(event) => setTableN(Number(event.target.value))}>
                {[10, 100, 1000, 10000, 1000000].map((n) => <option key={n} value={n}>{n.toLocaleString()}</option>)}
              </select>
            </label>
            <table className="complexity-table">
              <thead>
                <tr><th>Class</th><th>Operations</th><th>Time at 1 µs / op</th></tr>
              </thead>
              <tbody>
                {SERIES.map((s) => {
                  const ops = s.fn(tableN)
                  return (
                    <tr key={s.id} onMouseEnter={() => setFocus(s.id)} onMouseLeave={() => setFocus(null)}>
                      <td><code>{s.id}</code></td>
                      <td>{Number.isFinite(ops) ? format(ops) : '∞'}</td>
                      <td>{Number.isFinite(ops) ? duration(ops) : 'longer than the universe'}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        </div>
      }
      message={
        logScale
          ? 'On a log scale each grid line is 10× the last. 2ⁿ is still a straight, steep climb.'
          : 'Drag "n up to" higher and watch 2ⁿ and n² leave everything else behind.'
      }
      code={CODE}
      line={focused?.line}
    />
  )
}

export default Growth
