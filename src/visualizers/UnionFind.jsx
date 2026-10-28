import { useState } from 'react'
import { ArrayCells, GraphView, PlayerControls, VizLayout } from './common'
import { layoutTree, useStepPlayer } from './helpers'

const CODE = `parent = list(range(n))
size = [1] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])   # path compression
    return parent[x]

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra                   # smaller tree under larger
    size[ra] += size[rb]
    return True`

const N = 8

function findSteps(state, x, frames, label) {
  const path = []
  let node = x
  while (state.parent[node] !== node) {
    path.push(node)
    node = state.parent[node]
  }
  path.push(node)
  const root = node
  frames.push({ ...state, line: 5, message: `${label}find(${x}): follow parents ${path.join(' → ')}. Root is ${root}.`, path, current: x })

  const toCompress = path.slice(0, -1).filter((n) => state.parent[n] !== root)
  if (toCompress.length) {
    const parent = [...state.parent]
    toCompress.forEach((n) => { parent[n] = root })
    state = { ...state, parent }
    frames.push({ ...state, line: 6, message: `Path compression: point ${toCompress.join(', ')} straight at ${root}.`, path: [...toCompress, root], current: x })
  }
  return { state, root }
}

function unionSteps(start, a, b) {
  const frames = []
  let { state, root: ra } = findSteps(start, a, frames, '')
  const second = findSteps(state, b, frames, '')
  state = second.state
  let rb = second.root

  if (ra === rb) {
    frames.push({ ...state, line: 12, message: `${a} and ${b} already share root ${ra}. Nothing to merge (this edge would form a cycle).`, found: [ra] })
    return frames
  }
  if (state.size[ra] < state.size[rb]) [ra, rb] = [rb, ra]
  const parent = [...state.parent]
  const size = [...state.size]
  parent[rb] = ra
  size[ra] += size[rb]
  state = { parent, size }
  frames.push({ ...state, line: 15, message: `Attach root ${rb} (size ${size[ra] - size[rb]}) under root ${ra}. The group now has ${size[ra]} items.`, found: [ra, rb] })
  return frames
}

const INITIAL = {
  parent: Array.from({ length: N }, (_, i) => i),
  size: Array(N).fill(1),
}

function seeded() {
  let state = INITIAL
  for (const [a, b] of [[0, 1], [2, 3], [1, 3], [4, 5]]) state = unionSteps(state, a, b).at(-1)
  return { parent: state.parent, size: state.size }
}

const START = [{ ...seeded(), message: 'Union two items to merge their groups, or find an item\'s root.' }]

function UnionFind() {
  const [frames, setFrames] = useState(START)
  const [a, setA] = useState(6)
  const [b, setB] = useState(2)
  const player = useStepPlayer(frames, { autoPlay: true })
  const { frame } = player
  const latest = frames.at(-1)
  const state = { parent: latest.parent, size: latest.size }

  const valid = (x) => Number.isInteger(x) && x >= 0 && x < N

  const roots = frame.parent.map((p, i) => (p === i ? i : null)).filter((i) => i !== null)
  const children = (id) => frame.parent.map((p, i) => (p === id && i !== id ? i : null)).filter((i) => i !== null)
  const positions = layoutTree(roots, children, 56, 66)
  const nodes = frame.parent.map((p, i) => ({
    id: i,
    label: i,
    ...positions[i],
    state: frame.found?.includes(i)
      ? 'found'
      : frame.current === i
        ? 'comparing'
        : frame.path?.includes(i)
          ? 'pivot'
          : p === i ? 'sorted' : '',
  }))
  const edges = frame.parent
    .map((p, i) => (p !== i ? { from: i, to: p, state: frame.path?.includes(i) ? 'active' : '' } : null))
    .filter(Boolean)

  const groups = roots.length

  return (
    <VizLayout
      toolbar={
        <form className="inline-form" onSubmit={(event) => { event.preventDefault(); if (valid(a) && valid(b)) setFrames(unionSteps(state, a, b)) }}>
          <label><span>a</span><input type="number" min="0" max={N - 1} value={a} onChange={(e) => setA(Number(e.target.value))} /></label>
          <label><span>b</span><input type="number" min="0" max={N - 1} value={b} onChange={(e) => setB(Number(e.target.value))} /></label>
          <button className="button primary small" type="submit">union(a, b)</button>
          <button className="button ghost small" type="button" onClick={() => {
            if (!valid(a)) return
            const steps = []
            findSteps(state, a, steps, '')
            setFrames(steps)
          }}>find(a)</button>
          <button className="button ghost small" type="button" onClick={() => setFrames([{ ...INITIAL, message: 'Everyone starts in their own group.' }])}>Reset</button>
          <span className="stat-chips"><span>Groups <strong>{groups}</strong></span></span>
        </form>
      }
      visual={
        <div className="heap-view">
          <GraphView nodes={nodes} edges={edges} directed height={260} />
          <p className="muted center">parent array (arrows point from child to parent)</p>
          <ArrayCells frame={{ array: frame.parent, found: frame.found, pivot: frame.path }} />
        </div>
      }
      legend={[['sorted', 'Root'], ['comparing', 'Starting item'], ['pivot', 'Find path'], ['found', 'Roots being merged']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={{ parent: frame.parent, size: frame.size }}
    />
  )
}

export default UnionFind
