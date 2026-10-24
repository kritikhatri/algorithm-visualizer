import { useMemo, useState } from 'react'
import { GraphView, PlayerControls, VizLayout, useStepPlayer } from './common'

const PLAIN = `def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)`

const MEMO = `memo = {}

def fib(n):
    if n in memo:
        return memo[n]
    if n < 2:
        return n
    memo[n] = fib(n - 1) + fib(n - 2)
    return memo[n]`

// Line numbers for each event, per version of the code.
const LINES = {
  plain: { call: 1, base: 3, combine: 4 },
  memo: { call: 3, hit: 5, base: 7, combine: 8 },
}

function fibSteps(n, memoize) {
  const lines = LINES[memoize ? 'memo' : 'plain']
  const nodes = []
  const finished = {}
  const stack = []
  const memo = {}
  const frames = []

  const push = (line, message) =>
    frames.push({
      count: nodes.length,
      finished: { ...finished },
      stack: [...stack],
      line,
      message,
      vars: {
        n: stack.length ? nodes[stack.at(-1)].n : n,
        ...(memoize && { memo: { ...memo } }),
      },
    })

  function call(k, parent) {
    const id = nodes.length
    nodes.push({ id, n: k, parent })
    stack.push(id)
    push(lines.call, `Call fib(${k}).`)

    let result
    if (memoize && k in memo) {
      result = memo[k]
      finished[id] = { value: result, memo: true }
      push(lines.hit, `fib(${k}) is already in memo → ${result}. No more calls needed!`)
    } else if (k < 2) {
      result = k
      finished[id] = { value: result }
      push(lines.base, `Base case: fib(${k}) = ${k}.`)
    } else {
      const a = call(k - 1, id)
      const b = call(k - 2, id)
      result = a + b
      if (memoize) memo[k] = result
      finished[id] = { value: result }
      push(lines.combine, `fib(${k}) = ${a} + ${b} = ${result}.`)
    }
    stack.pop()
    return result
  }

  const answer = call(n, null)
  push(lines.combine, `Done: fib(${n}) = ${answer} using ${nodes.length} calls${memoize ? ' thanks to memoization' : ''}.`)
  return { nodes, frames }
}

// Leaves get consecutive x positions; parents sit centred above their children.
function layout(nodes) {
  const children = {}
  nodes.forEach((node) => node.parent !== null && (children[node.parent] ??= []).push(node.id))
  const positions = {}
  let leaf = 0
  function place(id, depth) {
    const kids = children[id] ?? []
    kids.forEach((kid) => place(kid, depth + 1))
    const x = kids.length
      ? kids.reduce((sum, kid) => sum + positions[kid].x, 0) / kids.length
      : leaf++ * 52
    positions[id] = { x, y: depth * 70 }
  }
  place(0, 0)
  return positions
}

function RecursionTree() {
  const [n, setN] = useState(5)
  const [memoize, setMemoize] = useState(false)

  const { nodes, frames } = useMemo(() => fibSteps(n, memoize), [n, memoize])
  const positions = useMemo(() => layout(nodes), [nodes])
  const player = useStepPlayer(frames)
  const { frame } = player

  const visible = nodes.slice(0, frame.count)
  const top = frame.stack.at(-1)
  const graphNodes = visible.map((node) => {
    const done = frame.finished[node.id]
    return {
      id: node.id,
      label: `f(${node.n})`,
      note: done ? `= ${done.value}` : undefined,
      x: positions[node.id].x,
      y: positions[node.id].y,
      state: node.id === top ? 'comparing' : done?.memo ? 'found' : done ? 'sorted' : 'pivot',
    }
  })
  const edges = visible
    .filter((node) => node.parent !== null)
    .map((node) => ({ from: node.parent, to: node.id }))

  return (
    <VizLayout
      toolbar={
        <>
          <label className="inline-field">
            <span>n</span>
            <select value={n} onChange={(event) => setN(Number(event.target.value))}>
              {[2, 3, 4, 5, 6, 7].map((value) => <option key={value}>{value}</option>)}
            </select>
          </label>
          <label className="checkbox">
            <input type="checkbox" checked={memoize} onChange={(event) => setMemoize(event.target.checked)} />
            Use memoization
          </label>
          <span className="stat-chips">
            <span>Total calls <strong>{nodes.length}</strong></span>
          </span>
        </>
      }
      visual={<GraphView nodes={graphNodes} edges={edges} directed height={380} />}
      legend={[
        ['comparing', 'Running now'],
        ['pivot', 'Waiting on children'],
        ['sorted', 'Returned'],
        ['found', 'Memo hit'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={memoize ? MEMO : PLAIN}
      line={frame.line}
      vars={frame.vars}
      extra={
        <section className="card">
          <h2 className="card-title">Call stack</h2>
          <ol className="call-stack">
            {frame.stack.length === 0 && <li className="muted">empty</li>}
            {[...frame.stack].reverse().map((id, i) => (
              <li key={id} className={i === 0 ? 'top' : ''}>fib({nodes[id].n})</li>
            ))}
          </ol>
        </section>
      }
    />
  )
}

export default RecursionTree
