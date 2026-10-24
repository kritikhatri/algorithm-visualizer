import { formatArgs, pyRepr } from '../utils/format'

function TestResults({ outcome }) {
  if (outcome.error) {
    return (
      <section className="card results failed">
        <h2 className="card-title">Error</h2>
        <pre className="output"><span className="output-error">{outcome.error}</span></pre>
      </section>
    )
  }

  const passed = outcome.results.filter((r) => r.passed).length
  const allPassed = passed === outcome.results.length

  return (
    <section className={`card results ${allPassed ? 'passed' : 'failed'}`} aria-live="polite">
      <h2 className="card-title">
        {allPassed ? '✓ All tests passed!' : `${passed} / ${outcome.results.length} tests passed`}
      </h2>

      <ol className="test-list">
        {outcome.results.map((result, i) => (
          <li key={i} className={`test ${result.passed ? 'pass' : 'fail'}`}>
            <span className="test-icon">{result.passed ? '✓' : '✗'}</span>
            <div className="test-body">
              <code>Input: {formatArgs(result.input)}</code>
              <code>Expected: {pyRepr(result.expected)}</code>
              {!result.passed && !result.error && <code>Got: {pyRepr(result.got)}</code>}
              {result.error && <pre className="output-error">{result.error}</pre>}
              {result.stdout && <pre className="test-stdout">{result.stdout}</pre>}
            </div>
          </li>
        ))}
      </ol>
    </section>
  )
}

export default TestResults
