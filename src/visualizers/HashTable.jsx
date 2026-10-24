import { useState } from 'react'
import { PlayerControls, VizLayout, useStepPlayer } from './common'

const SIZE = 7

const CODE = `class HashSet:
    def __init__(self, size=7):
        self.buckets = [[] for _ in range(size)]

    def _hash(self, key):
        return sum(ord(ch) for ch in key) % len(self.buckets)

    def add(self, key):
        bucket = self.buckets[self._hash(key)]
        if key not in bucket:
            bucket.append(key)

    def contains(self, key):
        bucket = self.buckets[self._hash(key)]
        return key in bucket`

function hashParts(key) {
  const codes = [...key].map((ch) => ch.charCodeAt(0))
  const total = codes.reduce((sum, code) => sum + code, 0)
  return { codes, total, index: total % SIZE }
}

function operationSteps(buckets, key, op) {
  const frames = []
  const { codes, total, index } = hashParts(key)
  const bucket = buckets[index]
  const isAdd = op === 'add'
  const push = (line, message, extra = {}) =>
    frames.push({ buckets, line, message, active: index, vars: { key, index }, ...extra })

  push(6, `hash("${key}") = ${codes.join(' + ')} = ${total}, and ${total} % ${SIZE} = ${index}.`)
  push(isAdd ? 9 : 14, `Jump straight to bucket ${index}. No scanning other buckets!`, { vars: { key, index, bucket } })

  for (let i = 0; i < bucket.length; i++) {
    const match = bucket[i] === key
    push(isAdd ? 10 : 15, `Compare "${key}" with "${bucket[i]}": ${match ? 'match!' : 'different.'}`, {
      scan: i,
      found: match ? i : undefined,
      vars: { key, index, bucket },
    })
    if (match) {
      push(isAdd ? 10 : 15, isAdd
        ? `"${key}" is already in the set. Sets store each key once.`
        : `contains("${key}") → True`, { found: i, vars: { key, index, result: isAdd ? undefined : true } })
      return frames
    }
  }

  if (!isAdd) {
    push(15, `Reached the end of bucket ${index}. contains("${key}") → False`, { vars: { key, index, result: false } })
    return frames
  }

  const next = buckets.map((b, i) => (i === index ? [...b, key] : b))
  push(11, bucket.length
    ? `Collision: bucket ${index} already holds ${bucket.length} key(s). Chain "${key}" onto the end.`
    : `Bucket ${index} is empty. Store "${key}" there.`, {
    buckets: next,
    found: bucket.length,
    vars: { key, index, bucket: next[index] },
  })
  return frames
}

function initialBuckets() {
  let buckets = Array.from({ length: SIZE }, () => [])
  for (const word of ['cat', 'dog', 'bird', 'act']) {
    buckets = operationSteps(buckets, word, 'add').at(-1).buckets
  }
  return buckets
}

const START = [{ buckets: initialBuckets(), message: 'Add or look up a word. "cat" and "act" share a bucket because their letters sum to the same value.' }]

function HashTable() {
  const [frames, setFrames] = useState(START)
  const [word, setWord] = useState('tac')
  const [error, setError] = useState('')
  const player = useStepPlayer(frames, { autoPlay: true })
  const { frame } = player

  function run(op) {
    const key = word.trim().toLowerCase()
    if (!/^[a-z]{1,10}$/.test(key)) {
      setError('Use 1–10 letters.')
      return
    }
    setError('')
    setFrames(operationSteps(frames.at(-1).buckets, key, op))
  }

  return (
    <VizLayout
      toolbar={
        <form className="inline-form" onSubmit={(event) => { event.preventDefault(); run('add') }}>
          <label>
            <span>Key</span>
            <input value={word} onChange={(event) => setWord(event.target.value)} maxLength={10} />
          </label>
          <button className="button primary small" type="submit">add()</button>
          <button className="button ghost small" type="button" onClick={() => run('contains')}>contains()</button>
          <button className="button ghost small" type="button" onClick={() => setFrames(START)}>Reset</button>
          {error && <span className="error-text">{error}</span>}
        </form>
      }
      visual={
        <div className="buckets">
          {frame.buckets.map((bucket, i) => (
            <div className={`bucket ${frame.active === i ? 'active' : ''}`} key={i}>
              <span className="bucket-index">{i}</span>
              <div className="chain">
                {bucket.length === 0 && <span className="muted">empty</span>}
                {bucket.map((key, j) => (
                  <span
                    key={key}
                    className={`chain-item ${frame.active === i && frame.found === j ? 'found' : frame.active === i && frame.scan === j ? 'comparing' : ''}`}
                  >
                    {key}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      }
      legend={[['comparing', 'Comparing'], ['found', 'Match / inserted']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default HashTable
