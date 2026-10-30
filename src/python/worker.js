/* global importScripts, loadPyodide */
// Runs Python in a Web Worker so infinite loops can be stopped by terminating the worker.

// v0.27.7 (Python 3.12). The newer v314 CDN build fails to load inside workers.
const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/'

importScripts(`${PYODIDE_URL}pyodide.js`)

let pyodide

self.onmessage = async ({ data }) => {
  const { id, type } = data

  try {
    if (type === 'init') {
      pyodide = await loadPyodide({ indexURL: PYODIDE_URL })
      pyodide.runPython(data.harness)
      self.postMessage({ id, ok: true })
      return
    }

    const name = { test: 'run_tests', run: 'run_code', trace: 'trace_code' }[type]
    const fn = pyodide.globals.get(name)
    const args = type === 'run' ? [data.code] : [data.code, JSON.stringify(data.problem)]
    if (type === 'trace') args.push(data.testIndex)
    const output = fn(...args)
    fn.destroy()
    self.postMessage({ id, ok: true, result: JSON.parse(output) })
  } catch (error) {
    self.postMessage({ id, ok: false, error: String(error?.message ?? error) })
  }
}
