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

    const fn = pyodide.globals.get(type === 'test' ? 'run_tests' : 'run_code')
    const output =
      type === 'test' ? fn(data.code, JSON.stringify(data.problem)) : fn(data.code)
    fn.destroy()
    self.postMessage({ id, ok: true, result: JSON.parse(output) })
  } catch (error) {
    self.postMessage({ id, ok: false, error: String(error?.message ?? error) })
  }
}
