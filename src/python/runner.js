import { useSyncExternalStore } from 'react'
import harnessSource from './harness.py?raw'

const TIME_LIMIT_MS = 8000

let worker = null
let ready = null
let status = 'idle' // idle | loading | ready | error
let nextId = 1
const pending = new Map()
const listeners = new Set()

function setStatus(value) {
  status = value
  listeners.forEach((listener) => listener())
}

function send(message) {
  const id = nextId++
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject })
    worker.postMessage({ ...message, id })
  })
}

function startWorker() {
  worker = new Worker(new URL('./worker.js', import.meta.url))
  worker.onmessage = ({ data }) => {
    const request = pending.get(data.id)
    pending.delete(data.id)
    if (data.ok) request?.resolve(data.result)
    else request?.reject(new Error(data.error))
  }
  worker.onerror = () => {
    setStatus('error')
    pending.forEach(({ reject }) => reject(new Error('Python failed to load. Check your connection.')))
    pending.clear()
  }

  setStatus('loading')
  ready = send({ type: 'init', harness: harnessSource }).then(
    () => setStatus('ready'),
    (error) => {
      setStatus('error')
      throw error
    }
  )
}

function stopWorker() {
  worker?.terminate()
  worker = null
  ready = null
  pending.forEach(({ reject }) => reject(new Error('Stopped.')))
  pending.clear()
}

export function loadPython() {
  if (!worker || status === 'error') startWorker()
  return ready
}

async function run(message) {
  await loadPython()

  let timer
  const timeout = new Promise((_, reject) => {
    timer = setTimeout(() => {
      stopWorker()
      setStatus('idle')
      reject(new Error(`Time limit exceeded (${TIME_LIMIT_MS / 1000}s). Is there an infinite loop?`))
    }, TIME_LIMIT_MS)
  })

  try {
    return await Promise.race([send(message), timeout])
  } finally {
    clearTimeout(timer)
  }
}

export function runTests(code, problem) {
  return run({ type: 'test', code, problem })
}

export function runTrace(code, problem, testIndex) {
  return run({ type: 'trace', code, problem, testIndex })
}

export function runCode(code) {
  return run({ type: 'run', code })
}

export function usePythonStatus() {
  return useSyncExternalStore(
    (listener) => {
      listeners.add(listener)
      return () => listeners.delete(listener)
    },
    () => status
  )
}
