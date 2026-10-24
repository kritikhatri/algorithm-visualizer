import { useMemo, useState } from 'react'
import { GraphView, PlayerControls, VizLayout, useStepPlayer } from './common'

const BFS = `from collections import deque

def bfs(graph, start):
    seen = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return order`

const DFS = `def dfs(graph, start):
    seen = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        order.append(node)
        for nxt in reversed(graph[node]):
            if nxt not in seen:
                stack.append(nxt)
    return order`

const POSITIONS = {
  A: [0, 90], B: [130, 10], C: [130, 170], D: [270, 60],
  E: [270, 200], F: [410, 10], G: [410, 150], H: [540, 90],
}

const EDGES = [
  ['A', 'B'], ['A', 'C'], ['B', 'D'], ['C', 'D'], ['C', 'E'],
  ['D', 'F'], ['D', 'G'], ['E', 'G'], ['F', 'H'], ['G', 'H'],
]

const GRAPH = Object.fromEntries(Object.keys(POSITIONS).map((node) => [node, []]))
for (const [a, b] of EDGES) {
  GRAPH[a].push(b)
  GRAPH[b].push(a)
}
Object.values(GRAPH).forEach((list) => list.sort())

const edgeKey = (a, b) => [a, b].sort().join('')

function bfsSteps(start) {
  const frames = []
  const seen = new Set([start])
  const queue = [start]
  const order = []
  const tree = new Set()
  const push = (line, message, extra = {}) =>
    frames.push({
      line,
      message,
      seen: [...seen],
      frontier: [...queue],
      order: [...order],
      tree: [...tree],
      vars: { queue: [...queue], order: [...order], seen: [...seen].sort() },
      ...extra,
    })

  push(5, `Start at ${start}: mark it seen and put it in the queue.`)
  while (queue.length) {
    const node = queue.shift()
    push(8, `Dequeue ${node} from the front.`, { current: node })
    order.push(node)
    push(9, `Visit ${node}.`, { current: node })
    for (const nxt of GRAPH[node]) {
      if (seen.has(nxt)) {
        push(11, `Neighbour ${nxt} was already seen. Skip it.`, { current: node, edge: edgeKey(node, nxt) })
      } else {
        seen.add(nxt)
        queue.push(nxt)
        tree.add(edgeKey(node, nxt))
        push(13, `Neighbour ${nxt} is new: mark it seen and enqueue it.`, { current: node, edge: edgeKey(node, nxt) })
      }
    }
  }
  push(14, `Done. BFS visits nodes in order of distance from ${start}: ${order.join(' → ')}.`)
  return frames
}

function dfsSteps(start) {
  const frames = []
  const seen = new Set()
  const stack = [[start, null]]
  const order = []
  const tree = new Set()
  const push = (line, message, extra = {}) =>
    frames.push({
      line,
      message,
      seen: [...seen],
      frontier: stack.map(([node]) => node),
      order: [...order],
      tree: [...tree],
      vars: { stack: stack.map(([node]) => node), order: [...order], seen: [...seen].sort() },
      ...extra,
    })

  push(3, `Push the start node ${start} onto the stack.`)
  while (stack.length) {
    const [node, parent] = stack.pop()
    push(6, `Pop ${node} from the top of the stack.`, { current: node })
    if (seen.has(node)) {
      push(8, `${node} was already visited. Skip it.`, { current: node })
      continue
    }
    seen.add(node)
    order.push(node)
    if (parent) tree.add(edgeKey(parent, node))
    push(10, `Visit ${node}.`, { current: node })
    for (const nxt of [...GRAPH[node]].reverse()) {
      if (!seen.has(nxt)) {
        stack.push([nxt, node])
        push(13, `Push unvisited neighbour ${nxt}.`, { current: node, edge: edgeKey(node, nxt) })
      }
    }
  }
  push(14, `Done. DFS dives deep first: ${order.join(' → ')}.`)
  return frames
}

function GraphTraversal() {
  const [algorithm, setAlgorithm] = useState('bfs')
  const [start, setStart] = useState('A')
  const frames = useMemo(() => (algorithm === 'bfs' ? bfsSteps(start) : dfsSteps(start)), [algorithm, start])
  const player = useStepPlayer(frames)
  const { frame } = player

  const nodes = Object.entries(POSITIONS).map(([id, [x, y]]) => ({
    id,
    label: id,
    x,
    y,
    state: frame.current === id
      ? 'comparing'
      : frame.order.includes(id)
        ? 'sorted'
        : frame.frontier.includes(id)
          ? 'pivot'
          : '',
  }))
  const edges = EDGES.map(([from, to]) => {
    const key = edgeKey(from, to)
    return { from, to, state: frame.edge === key ? 'active' : frame.tree.includes(key) ? 'tree' : '' }
  })

  return (
    <VizLayout
      toolbar={
        <>
          <div className="tabs compact" role="group" aria-label="Algorithm">
            {[['bfs', 'Breadth-first'], ['dfs', 'Depth-first']].map(([id, label]) => (
              <button key={id} className={`tab ${algorithm === id ? 'active' : ''}`} aria-pressed={algorithm === id} onClick={() => setAlgorithm(id)}>
                {label}
              </button>
            ))}
          </div>
          <span className="muted">Click a node to start from it.</span>
        </>
      }
      visual={<GraphView nodes={nodes} edges={edges} height={300} onNodeClick={setStart} />}
      legend={[
        ['comparing', 'Current'],
        ['pivot', algorithm === 'bfs' ? 'In queue' : 'On stack'],
        ['sorted', 'Visited'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={algorithm === 'bfs' ? BFS : DFS}
      line={frame.line}
      vars={frame.vars}
      extra={
        <section className="card">
          <h2 className="card-title">Adjacency list</h2>
          <dl className="vars">
            {Object.entries(GRAPH).map(([node, list]) => (
              <div key={node}><dt>{node}</dt><dd>{list.join(', ')}</dd></div>
            ))}
          </dl>
        </section>
      }
    />
  )
}

export default GraphTraversal
