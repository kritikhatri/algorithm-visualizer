import { useState } from 'react'
import { runTrace } from '../python/runner'
import { PlayerControls } from '../visualizers/common'
import { useStepPlayer } from '../visualizers/helpers'
import { formatArgs } from '../utils/format'
import CodeEditor from './CodeEditor'

function TracePlayer({ code, steps }) {
  const player = useStepPlayer(steps)
  const { frame } = player

  return (
    <>
      <p className="viz-message">
        {frame.returned !== undefined
          ? `${frame.function}() returns ${frame.returned}`
          : `In ${frame.function}(), about to run line ${frame.line}`}
        {frame.depth > 0 && ` · recursion depth ${frame.depth}`}
      </p>
      <CodeEditor value={code} readOnly activeLine={frame.line} />
      <dl className="vars">
        {Object.entries(frame.vars).map(([name, value]) => (
          <div key={name}><dt>{name}</dt><dd>{value}</dd></div>
        ))}
      </dl>
      <PlayerControls player={player} />
    </>
  )
}

function CodeTracer({ code, problem }) {
  const [testIndex, setTestIndex] = useState(0)
  const [trace, setTrace] = useState(null)
  const [running, setRunning] = useState(false)

  async function handleTrace() {
    setRunning(true)
    try {
      setTrace({ code, ...(await runTrace(code, problem, testIndex)) })
    } catch (err) {
      setTrace({ code, steps: [], error: err.message })
    }
    setRunning(false)
  }

  const label = (test, i) =>
    `Test ${i + 1}${test.ops ? '' : `: ${formatArgs(test.args).slice(0, 40)}`}`

  return (
    <section className="card tracer">
      <h2 className="card-title">Visualize my code</h2>
      <div className="toolbar-actions">
        <select aria-label="Test case" value={testIndex} onChange={(e) => setTestIndex(Number(e.target.value))}>
          {problem.tests.map((test, i) => <option key={i} value={i}>{label(test, i)}</option>)}
        </select>
        <button className="button ghost small" onClick={handleTrace} disabled={running}>
          {running ? 'Tracing…' : '🔍 Trace'}
        </button>
      </div>

      {trace?.error && <pre className="output"><span className="output-error">{trace.error}</span></pre>}
      {trace?.truncated && <p className="muted small-note">Showing the first 500 steps only.</p>}
      {trace && !trace.error && trace.steps.length === 0 && <p className="muted">Nothing ran. Is the function body empty?</p>}
      {trace?.steps.length > 0 && <TracePlayer key={trace.steps.length + trace.code} code={trace.code} steps={trace.steps} />}
    </section>
  )
}

export default CodeTracer
