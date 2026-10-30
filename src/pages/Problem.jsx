import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../auth'
import { useApi } from '../useApi'
import { loadPython, runTests, usePythonStatus } from '../python/runner'
import CodeEditor from '../components/CodeEditor'
import Difficulty from '../components/Difficulty'
import Markdown from '../components/Markdown'
import InterviewTimer from '../components/InterviewTimer'
import TestResults from '../components/TestResults'
import NotFound from './NotFound'

const draftKey = (id) => `dsa-draft-${id}`

function readDraft(id) {
  try {
    return localStorage.getItem(draftKey(id))
  } catch {
    return null
  }
}

function writeDraft(id, code) {
  try {
    localStorage.setItem(draftKey(id), code)
  } catch {
    // Drafts are a convenience; ignore storage errors.
  }
}

function Problem() {
  const { problemId } = useParams()
  const { data, error } = useApi(`/problems/${problemId}`)

  if (error?.status === 404) return <NotFound />
  if (error) return <p className="card error-text">{error.message}</p>
  if (!data) return <p className="muted">Loading…</p>

  return <Workspace key={data.problem.id} problem={data.problem} />
}

function Workspace({ problem }) {
  const { user, progress, openAuth, refreshProgress } = useAuth()
  const pythonStatus = usePythonStatus()
  const [code, setCode] = useState(() => readDraft(problem.id) ?? problem.starter)
  const [outcome, setOutcome] = useState(null)
  const [running, setRunning] = useState(false)
  const [hintsShown, setHintsShown] = useState(0)
  const [showSolution, setShowSolution] = useState(false)

  const solved = progress?.solvedProblems.includes(problem.id)

  useEffect(() => {
    loadPython().catch(() => {})
  }, [])

  // Logged-in learners get their last saved attempt from the server.
  useEffect(() => {
    if (!user) return
    api(`/problems/${problem.id}/progress`)
      .then((saved) => saved.code && setCode(saved.code))
      .catch(() => {})
  }, [user, problem.id])

  function handleChange(value) {
    setCode(value)
    writeDraft(problem.id, value)
  }

  async function handleRun() {
    setRunning(true)
    try {
      const result = await runTests(code, problem)
      setOutcome(result)
      const passed = !result.error && result.results.every((r) => r.passed)
      if (user) {
        await api(`/problems/${problem.id}/progress`, { method: 'PUT', body: { code, passed } })
        refreshProgress()
      }
    } catch (err) {
      setOutcome({ error: err.message, results: [] })
    }
    setRunning(false)
  }

  function handleReset() {
    handleChange(problem.starter)
    setOutcome(null)
  }

  const runLabel = running
    ? 'Running…'
    : pythonStatus === 'loading'
      ? 'Loading Python…'
      : '▶ Run tests'

  return (
    <div
      className="workspace"
      onKeyDown={(event) => {
        if ((event.metaKey || event.ctrlKey) && event.key === 'Enter' && !running) {
          event.preventDefault()
          handleRun()
        }
      }}
    >
      <section className="card statement">
        <Link to={`/topics/${problem.topic}/practice`} className="back-link">← Back to topic</Link>
        <div className="statement-head">
          <h1>{problem.title}</h1>
          <Difficulty level={problem.difficulty} />
          {solved && <span className="done-badge">✓ Solved</span>}
        </div>

        <Markdown source={problem.statement} />

        <div className="hints">
          {problem.hints.slice(0, hintsShown).map((hint, i) => (
            <p className="hint" key={i}><strong>Hint {i + 1}:</strong> {hint}</p>
          ))}
          {hintsShown < problem.hints.length && (
            <button className="button ghost small" onClick={() => setHintsShown(hintsShown + 1)}>
              💡 Show {hintsShown ? 'another' : 'a'} hint
            </button>
          )}
        </div>

        <div className="solution">
          {showSolution ? (
            <>
              <h2 className="card-title">Reference solution</h2>
              <CodeEditor value={problem.solution} readOnly />
            </>
          ) : (
            <button className="button ghost small" onClick={() => setShowSolution(true)}>
              Reveal solution
            </button>
          )}
        </div>
      </section>

      <section className="editor-pane">
        <div className="card editor-card">
          <div className="editor-toolbar">
            <span className="muted">solution.py · Python 3</span>
            <div className="toolbar-actions">
              <InterviewTimer />
              <button className="button ghost small" onClick={handleReset}>Reset</button>
              <button className="button primary small" onClick={handleRun} disabled={running}>
                {runLabel}
              </button>
            </div>
          </div>
          <CodeEditor value={code} onChange={handleChange} minHeight="320px" />
        </div>

        {pythonStatus === 'error' && (
          <p className="error-text">Couldn't download Python. Check your internet connection and try again.</p>
        )}

        {outcome ? (
          <TestResults outcome={outcome} />
        ) : (
          <p className="muted small-note">
            Tests run locally in your browser with Pyodide. The first run downloads Python (~10 MB).
            {!user && (
              <> <button className="link" onClick={openAuth}>Log in</button> to save your solutions.</>
            )}
          </p>
        )}
      </section>
    </div>
  )
}

export default Problem
