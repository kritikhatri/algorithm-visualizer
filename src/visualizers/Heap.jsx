import { useState } from 'react'
import { ArrayCells, GraphView, PlayerControls, VizLayout } from './common'
import { layoutBinaryTree, stateOf, useStepPlayer } from './helpers'

const CODE = `def push(heap, val):
    heap.append(val)
    i = len(heap) - 1
    while i > 0 and heap[(i - 1) // 2] > heap[i]:
        parent = (i - 1) // 2
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent

def pop(heap):
    heap[0], heap[-1] = heap[-1], heap[0]
    smallest = heap.pop()
    i = 0
    while True:
        left, right, best = 2 * i + 1, 2 * i + 2, i
        if left < len(heap) and heap[left] < heap[best]:
            best = left
        if right < len(heap) and heap[right] < heap[best]:
            best = right
        if best == i:
            return smallest
        heap[i], heap[best] = heap[best], heap[i]
        i = best`

const LIMIT = 15

function pushSteps(start, val) {
  const heap = [...start, val]
  const frames = []
  const push = (line, message, extra = {}) => frames.push({ array: [...heap], line, message, ...extra })
  let i = heap.length - 1
  push(2, `Append ${val} at the end (index ${i}) so the tree stays complete.`, { found: [i], vars: { val, i } })

  while (i > 0) {
    const parent = Math.floor((i - 1) / 2)
    push(4, `Compare ${heap[i]} with its parent ${heap[parent]}.`, { comparing: [i, parent], vars: { val, i, parent } })
    if (heap[parent] <= heap[i]) {
      push(4, `Parent ${heap[parent]} ≤ ${heap[i]}: the heap property holds. Done.`, { found: [i], vars: { val, i } })
      return frames
    }
    ;[heap[i], heap[parent]] = [heap[parent], heap[i]]
    push(6, `${heap[parent]} is smaller than its parent, so swap them (sift up).`, { swapping: [i, parent], vars: { val, i, parent } })
    i = parent
  }
  push(4, `${val} reached the root. It's the new minimum.`, { found: [0], vars: { val, i } })
  return frames
}

function popSteps(start) {
  const heap = [...start]
  const frames = []
  const push = (line, message, extra = {}) => frames.push({ array: [...heap], line, message, ...extra })
  const last = heap.length - 1

  ;[heap[0], heap[last]] = [heap[last], heap[0]]
  push(10, `Swap the root with the last item so the minimum sits at the end.`, { swapping: [0, last] })
  const smallest = heap.pop()
  push(11, `Remove ${smallest} from the end. That's our answer; now repair the heap.`, { vars: { smallest } })

  let i = 0
  while (heap.length) {
    const left = 2 * i + 1
    const right = 2 * i + 2
    let best = i
    if (left < heap.length && heap[left] < heap[best]) best = left
    if (right < heap.length && heap[right] < heap[best]) best = right
    const kids = [left, right].filter((k) => k < heap.length)
    push(14, kids.length
      ? `Compare ${heap[i]} with its children ${kids.map((k) => heap[k]).join(' and ')}.`
      : `${heap[i]} has no children.`, { comparing: [i, ...kids], vars: { smallest, i, left, right, best } })
    if (best === i) {
      push(20, `${heap[i]} is ≤ its children. Heap restored; return ${smallest}.`, { found: [i], vars: { smallest, i } })
      return frames
    }
    ;[heap[i], heap[best]] = [heap[best], heap[i]]
    push(21, `Swap ${heap[best]} down with its smaller child ${heap[i]} (sift down).`, { swapping: [i, best], vars: { smallest, i, best } })
    i = best
  }
  push(20, `The heap is now empty. Returned ${smallest}.`, { vars: { smallest } })
  return frames
}

function build(values) {
  return values.reduce((heap, value) => pushSteps(heap, value).at(-1).array, [])
}

const START = [{ array: build([8, 3, 10, 1, 6, 14, 4]), message: 'Push a value or pop the minimum.' }]

function Heap() {
  const [frames, setFrames] = useState(START)
  const [value, setValue] = useState(2)
  const player = useStepPlayer(frames, { autoPlay: true })
  const { frame } = player
  const heap = frames.at(-1).array

  function handlePush(event) {
    event.preventDefault()
    if (!Number.isInteger(value)) return
    if (heap.length >= LIMIT) {
      setFrames([{ array: heap, message: `The demo holds up to ${LIMIT} items. Pop some first.` }])
      return
    }
    setFrames(pushSteps(heap, value))
  }

  function handlePop() {
    setFrames(heap.length ? popSteps(heap) : [{ array: heap, message: 'IndexError: the heap is empty.' }])
  }

  const values = frame.array
  const positions = layoutBinaryTree(values.length ? 0 : null, (i) => [
    2 * i + 1 < values.length ? 2 * i + 1 : null,
    2 * i + 2 < values.length ? 2 * i + 2 : null,
  ])
  const nodes = values.map((v, i) => ({ id: i, label: v, ...positions[i], state: stateOf(i, frame) }))
  const edges = values.slice(1).map((_, k) => ({ from: Math.floor(k / 2), to: k + 1 }))

  return (
    <VizLayout
      toolbar={
        <form className="inline-form" onSubmit={handlePush}>
          <label>
            <span>Value</span>
            <input type="number" value={value} onChange={(event) => setValue(Number(event.target.value))} />
          </label>
          <button className="button primary small" type="submit">heappush</button>
          <button className="button ghost small" type="button" onClick={handlePop}>heappop</button>
          <button className="button ghost small" type="button" onClick={() => setFrames(START)}>Reset</button>
        </form>
      }
      visual={
        <div className="heap-view">
          <GraphView nodes={nodes} edges={edges} height={300} />
          <p className="muted center">Stored as a list: children of i are at 2i + 1 and 2i + 2</p>
          <ArrayCells frame={frame} />
        </div>
      }
      legend={[['comparing', 'Comparing'], ['swapping', 'Swapping'], ['found', 'Settled']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default Heap
