import { useState } from 'react'
import CodeEditor from '../components/CodeEditor'
import { pyRepr } from '../utils/format'
import { Raw, parseNumbers, stateOf } from './helpers'

export function PlayerControls({ player }) {
  if (player.total <= 1) return null

  const label = player.finished && player.total > 1
    ? '↻ Replay'
    : player.playing
      ? 'Ⅱ Pause'
      : player.index === 0
        ? '▶ Play'
        : '▶ Resume'

  return (
    <div className="playback">
      <div className="playback-buttons">
        <button className="button ghost icon" onClick={() => player.step(-1)} disabled={player.index === 0} aria-label="Previous step">←</button>
        <button className="button primary play" onClick={player.toggle}>{label}</button>
        <button className="button ghost icon" onClick={() => player.step(1)} disabled={player.finished} aria-label="Next step">→</button>
        <span className="step-pill">{player.index + 1} / {player.total}</span>
      </div>

      <label className="speed">
        <span>Speed</span>
        <input
          type="range"
          min="100"
          max="1500"
          step="100"
          // Reversed so dragging right means faster.
          value={1600 - player.speed}
          onChange={(event) => player.setSpeed(1600 - Number(event.target.value))}
        />
      </label>
    </div>
  )
}

/* ---------- Layout ---------- */

export function VizLayout({ toolbar, visual, legend, message, controls, code, line, vars, extra }) {
  return (
    <div className="viz">
      <section className="card viz-stage">
        {toolbar && <div className="viz-toolbar">{toolbar}</div>}
        <div className="viz-canvas">{visual}</div>
        {legend && <Legend items={legend} />}
        <p className="viz-message" aria-live="polite">{message || ' '}</p>
        {controls}
      </section>

      <aside className="viz-side">
        <section className="card viz-code">
          <h2 className="card-title">Python</h2>
          <CodeEditor value={code} readOnly activeLine={line} />
        </section>
        {vars && Object.keys(vars).length > 0 && (
          <section className="card">
            <h2 className="card-title">Variables</h2>
            <dl className="vars">
              {Object.entries(vars).map(([name, value]) => (
                <div key={name}>
                  <dt>{name}</dt>
                  <dd>{value instanceof Raw ? value.text : pyRepr(value)}</dd>
                </div>
              ))}
            </dl>
          </section>
        )}
        {extra}
      </aside>
    </div>
  )
}

export function Legend({ items }) {
  return (
    <div className="legend">
      {items.map(([state, label]) => (
        <span key={state}><i className={`legend-dot ${state}`} /> {label}</span>
      ))}
    </div>
  )
}

/* ---------- Arrays ---------- */

function pointerLabels(pointers = {}) {
  const byIndex = {}
  for (const [name, index] of Object.entries(pointers)) {
    if (index === null || index === undefined) continue
    ;(byIndex[index] ??= []).push(name)
  }
  return byIndex
}

export function ArrayBars({ frame }) {
  const values = frame.array
  const maxValue = Math.max(...values.map(Math.abs), 1)

  return (
    <div className="bars">
      {values.map((value, index) => (
        <div className="bar-slot" key={index}>
          <div
            className={`bar ${stateOf(index, frame)}`}
            style={{ height: `${Math.max((Math.abs(value) / maxValue) * 100, 6)}%` }}
          />
          <span className="bar-label">{value}</span>
        </div>
      ))}
    </div>
  )
}

export function ArrayCells({ frame, onCellClick }) {
  const labels = pointerLabels(frame.pointers)
  const Cell = onCellClick ? 'button' : 'div'

  return (
    <div className="cells">
      {frame.array.map((value, index) => (
        <div className="cell-slot" key={index}>
          <span className="cell-index">{index}</span>
          <Cell
            className={`cell ${stateOf(index, frame)}`}
            onClick={onCellClick && (() => onCellClick(value, index))}
          >
            {value}
          </Cell>
          <span className="cell-pointer">{labels[index]?.join(' · ')}</span>
        </div>
      ))}
    </div>
  )
}

/* ---------- Node-link diagrams (trees, graphs) ---------- */

export function GraphView({ nodes, edges, directed = false, height = 320, onNodeClick }) {
  if (nodes.length === 0) return <p className="muted center">Empty. Add some values.</p>

  const xs = nodes.map((n) => n.x)
  const ys = nodes.map((n) => n.y)
  const pad = 40
  const minX = Math.min(...xs) - pad
  const minY = Math.min(...ys) - pad
  const width = Math.max(Math.max(...xs) - minX + pad, 200)
  const viewHeight = Math.max(Math.max(...ys) - minY + pad, 120)
  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]))

  return (
    <svg
      className="graph"
      viewBox={`${minX} ${minY} ${width} ${viewHeight}`}
      style={{ maxHeight: height }}
      role="img"
      aria-label="Diagram"
    >
      <defs>
        <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M 0 0 L 10 5 L 0 10 z" className="arrow-head" />
        </marker>
      </defs>
      {edges.map((edge) => {
        const a = byId[edge.from]
        const b = byId[edge.to]
        if (!a || !b) return null
        const dx = b.x - a.x
        const dy = b.y - a.y
        const length = Math.hypot(dx, dy) || 1
        const r = 22
        return (
          <line
            key={`${edge.from}-${edge.to}`}
            className={`edge ${edge.state ?? ''}`}
            x1={a.x + (dx / length) * r}
            y1={a.y + (dy / length) * r}
            x2={b.x - (dx / length) * (r + (directed ? 4 : 0))}
            y2={b.y - (dy / length) * (r + (directed ? 4 : 0))}
            markerEnd={directed ? 'url(#arrow)' : undefined}
          />
        )
      })}
      {nodes.map((node) => (
        <g
          key={node.id}
          className={`node ${node.state ?? ''} ${onNodeClick ? 'clickable' : ''}`}
          transform={`translate(${node.x} ${node.y})`}
          onClick={onNodeClick && (() => onNodeClick(node.id))}
        >
          <circle r="20" />
          <text dy="0.35em">{node.label}</text>
          {node.note !== undefined && (
            <text className="node-note" dy="2.6em">{node.note}</text>
          )}
        </g>
      ))}
    </svg>
  )
}

/* ---------- Inputs ---------- */

export function NumberListInput({ initial, onSubmit, label = 'Values', maxLength, min, max, buttonLabel = 'Load' }) {
  const [text, setText] = useState(initial.join(', '))
  const [error, setError] = useState('')

  function handleSubmit(event) {
    event.preventDefault()
    const result = parseNumbers(text, { maxLength, min, max })
    setError(result.error ?? '')
    if (result.values) onSubmit(result.values)
  }

  return (
    <form className="inline-form" onSubmit={handleSubmit}>
      <label>
        <span>{label}</span>
        <input value={text} onChange={(event) => setText(event.target.value)} />
      </label>
      <button className="button ghost small" type="submit">{buttonLabel}</button>
      {error && <span className="error-text">{error}</span>}
    </form>
  )
}
