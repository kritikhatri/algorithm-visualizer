import { useState } from 'react'
import { runCode } from '../python/runner'
import CodeEditor from './CodeEditor'
import OutputPanel from './OutputPanel'

function CodeSnippet({ title, code }) {
  const [output, setOutput] = useState(null)
  const [running, setRunning] = useState(false)

  async function handleRun() {
    setRunning(true)
    try {
      setOutput(await runCode(code))
    } catch (error) {
      setOutput({ stdout: '', error: error.message })
    }
    setRunning(false)
  }

  return (
    <figure className="snippet">
      <figcaption className="snippet-head">
        <span>{title}</span>
        <button className="button ghost small" onClick={handleRun} disabled={running}>
          {running ? 'Running…' : '▶ Run'}
        </button>
      </figcaption>
      <CodeEditor value={code} readOnly />
      {output && <OutputPanel output={output} />}
    </figure>
  )
}

export default CodeSnippet
