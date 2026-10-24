function OutputPanel({ output }) {
  const empty = !output.stdout && !output.error

  return (
    <pre className="output" aria-live="polite">
      {output.stdout}
      {output.error && <span className="output-error">{output.error}</span>}
      {empty && <span className="muted">(no output)</span>}
    </pre>
  )
}

export default OutputPanel
