import { useEffect, useState } from 'react'
import { loadPython, runCode, usePythonStatus } from '../python/runner'
import CodeEditor from '../components/CodeEditor'
import OutputPanel from '../components/OutputPanel'

const EXAMPLES = {
  'Hello, Python': `name = "DSA learner"
print(f"Hello, {name}!")

squares = [n * n for n in range(1, 6)]
print("squares:", squares)
`,
  'Stack & queue': `from collections import deque

stack = []
for item in ["a", "b", "c"]:
    stack.append(item)
print("pop:", stack.pop(), "→ stack is now", stack)

queue = deque([1, 2, 3])
queue.append(4)
print("popleft:", queue.popleft(), "→ queue is now", list(queue))
`,
  'Heap (heapq)': `import heapq

nums = [9, 4, 7, 1, 8]
heapq.heapify(nums)
print("min:", nums[0])
print("sorted via heap:", [heapq.heappop(nums) for _ in range(len(nums))])
`,
  'O(n) loop vs O(1) formula': `import time

def loop_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

def formula_sum(n):
    return n * (n - 1) // 2

for fn in (loop_sum, formula_sum):
    start = time.perf_counter()
    fn(1_000_000)
    print(f"{fn.__name__}: {(time.perf_counter() - start) * 1000:.2f} ms")
`,
}

const DEFAULT = 'Hello, Python'

function Playground() {
  const status = usePythonStatus()
  const [code, setCode] = useState(EXAMPLES[DEFAULT])
  const [output, setOutput] = useState(null)
  const [running, setRunning] = useState(false)

  useEffect(() => {
    loadPython().catch(() => {})
  }, [])

  async function handleRun() {
    setRunning(true)
    try {
      setOutput(await runCode(code))
    } catch (error) {
      setOutput({ stdout: '', error: error.message })
    }
    setRunning(false)
  }

  function handleKeyDown(event) {
    if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
      event.preventDefault()
      handleRun()
    }
  }

  return (
    <>
      <header className="page-header">
        <p className="eyebrow">Scratchpad</p>
        <h1>Python Playground</h1>
        <p className="subtitle left">
          Experiment freely. Code runs in your browser; press <kbd>⌘/Ctrl</kbd> + <kbd>Enter</kbd> to run.
        </p>
      </header>

      <div className="playground" onKeyDown={handleKeyDown}>
        <section className="card editor-card">
          <div className="editor-toolbar">
            <select
              aria-label="Load an example"
              defaultValue={DEFAULT}
              onChange={(event) => {
                setCode(EXAMPLES[event.target.value])
                setOutput(null)
              }}
            >
              {Object.keys(EXAMPLES).map((name) => <option key={name}>{name}</option>)}
            </select>
            <button className="button primary small" onClick={handleRun} disabled={running}>
              {running ? 'Running…' : status === 'loading' ? 'Loading Python…' : '▶ Run'}
            </button>
          </div>
          <CodeEditor value={code} onChange={setCode} minHeight="420px" />
        </section>

        <section className="card">
          <h2 className="card-title">Output</h2>
          {output ? (
            <OutputPanel output={output} />
          ) : (
            <p className="muted">
              {status === 'error'
                ? "Couldn't download Python. Check your connection."
                : 'Run your code to see printed output here.'}
            </p>
          )}
        </section>
      </div>
    </>
  )
}

export default Playground
