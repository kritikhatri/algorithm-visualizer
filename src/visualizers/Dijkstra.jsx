import { useMemo, useState } from 'react'
import { GraphView, PlayerControls, VizLayout } from './common'
import { raw, useStepPlayer } from './helpers'

const CODE = `import heapq

def dijkstra(graph, source):
    dist = {source: 0}
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nxt, weight in graph[node]:
            nd = d + weight
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist`

const POSITIONS = {
  A: [0, 110], B: [140, 10], C: [140, 210], D: [300, 10], E: [300, 210], F: [440, 110],
}

const EDGES = [
  ['A', 'B', 4], ['A', 'C', 2], ['B', 'C', 1], ['B', 'D', 5],
  ['C', 'E', 8], ['C', 'D', 8], ['D', 'E', 2], ['D', 'F', 6], ['E', 'F', 3],
]

const GRAPH = Object.fromEntries(Object.keys(POSITIONS).map((node) => [node, []]))
for (const [a, b, w] of EDGES) {
  GRAPH[a].push([b, w])
  GRAPH[b].push([a, w])
}
Object.values(GRAPH).forEach((list) => list.sort())

const key = (a, b) => [a, b].sort().join('')
const show = (dist) =>
  raw(`{${Object.keys(POSITIONS).map((n) => `'${n}': ${dist[n] ?? 'inf'}`).join(', ')}}`)

function dijkstraSteps(source) {
  const frames = []
  const dist = { [source]: 0 }
  const done = new Set()
  const via = {}
  let heap = [[0, source]]
  const push = (line, message, extra = {}) =>
    frames.push({
      line,
      message,
      dist: { ...dist },
      done: [...done],
      via: { ...via },
      vars: { heap: heap.map(([d, n]) => [d, n]) },
      ...extra,
    })

  push(5, `Start: dist[${source}] = 0, everything else is ∞.`)
  while (heap.length) {
    heap.sort((x, y) => x[0] - y[0] || x[1].localeCompare(y[1]))
    const [d, node] = heap.shift()
    if (d > dist[node] || done.has(node)) {
      push(9, `Popped (${d}, ${node}), but ${node} already has distance ${dist[node]}. Skip this stale entry.`, { current: node })
      continue
    }
    done.add(node)
    push(7, `Pop the closest node: ${node} at distance ${d}. Its distance is now final.`, { current: node })
    for (const [nxt, weight] of GRAPH[node]) {
      if (done.has(nxt)) continue
      const nd = d + weight
      const better = nd < (dist[nxt] ?? Infinity)
      if (better) {
        dist[nxt] = nd
        via[nxt] = node
        heap = [...heap, [nd, nxt]]
      }
      push(better ? 13 : 12, better
        ? `${node} → ${nxt}: ${d} + ${weight} = ${nd} is shorter. Update dist[${nxt}] = ${nd} and push it.`
        : `${node} → ${nxt}: ${d} + ${weight} = ${nd} is not better than ${dist[nxt]}.`, {
        current: node,
        edge: key(node, nxt),
        updated: better ? nxt : undefined,
      })
    }
  }
  push(15, `Done. Green edges form the shortest-path tree from ${source}.`)
  return frames
}

function Dijkstra() {
  const [source, setSource] = useState('A')
  const frames = useMemo(() => dijkstraSteps(source), [source])
  const player = useStepPlayer(frames)
  const { frame } = player

  const treeEdges = new Set(Object.entries(frame.via).map(([n, p]) => key(n, p)))
  const nodes = Object.entries(POSITIONS).map(([id, [x, y]]) => ({
    id,
    label: id,
    x,
    y,
    note: frame.dist[id] ?? '∞',
    state: frame.current === id
      ? 'comparing'
      : frame.updated === id
        ? 'swapping'
        : frame.done.includes(id)
          ? 'sorted'
          : frame.dist[id] !== undefined ? 'pivot' : '',
  }))
  const edges = EDGES.map(([from, to, w]) => ({
    from,
    to,
    label: w,
    state: frame.edge === key(from, to) ? 'active' : treeEdges.has(key(from, to)) ? 'tree' : '',
  }))

  return (
    <VizLayout
      toolbar={<span className="muted">Click a node to use it as the source. Numbers under nodes are current distances.</span>}
      visual={<GraphView nodes={nodes} edges={edges} height={320} onNodeClick={setSource} />}
      legend={[
        ['comparing', 'Being expanded'],
        ['swapping', 'Distance improved'],
        ['pivot', 'Discovered'],
        ['sorted', 'Final'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={{ ...frame.vars, dist: show(frame.dist) }}
    />
  )
}

export default Dijkstra
