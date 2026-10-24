import { useMemo, useState } from 'react'
import { NumberListInput, PlayerControls, VizLayout, raw, useStepPlayer } from './common'

const CODE = `def reverse_list(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev`

function reverseSteps(values) {
  const n = values.length
  const next = values.map((_, i) => (i < n - 1 ? i + 1 : null))
  const frames = []
  // undefined = not assigned yet in the Python code; null = None.
  let prev = null
  let curr
  let nxt

  const name = (i) => (i === null ? 'None' : `ListNode(${values[i]})`)
  const push = (line, message) => {
    const pointers = Object.fromEntries(
      Object.entries({ prev, curr, nxt }).filter(([, index]) => index !== undefined)
    )
    frames.push({
      next: [...next],
      line,
      message,
      pointers,
      vars: Object.fromEntries(Object.entries(pointers).map(([key, index]) => [key, raw(name(index))])),
    })
  }

  push(2, 'prev starts as None: the new list is empty.')
  curr = 0
  push(3, `curr starts at the head, ${values[0]}.`)

  while (curr !== null) {
    nxt = next[curr]
    push(5, `Save nxt = ${name(nxt)} so we don't lose the rest of the list.`)
    next[curr] = prev
    push(6, `Flip the arrow: ${values[curr]}.next now points to ${name(prev)}.`)
    prev = curr
    push(7, `Move prev forward to ${values[prev]}.`)
    curr = nxt
    push(8, curr === null ? 'Move curr to None. We reached the end.' : `Move curr forward to ${values[curr]}.`)
  }
  push(9, `Return prev: ${values[prev]} is the new head.`)
  return frames
}

function LinkedList() {
  const [values, setValues] = useState([1, 2, 3, 4, 5])
  const frames = useMemo(() => reverseSteps(values), [values])
  const player = useStepPlayer(frames)
  const { frame } = player
  const n = values.length

  // Pointer positions: -1 is the "None" slot on the left, n is the one on the right.
  const slotOf = (name, index) => (index === null ? (name === 'prev' ? -1 : n) : index)
  const labels = {}
  for (const [name, index] of Object.entries(frame.pointers)) {
    ;(labels[slotOf(name, index)] ??= []).push(name)
  }

  const connector = (i) =>
    frame.next[i] === i + 1 ? '→' : frame.next[i + 1] === i ? '←' : ''

  return (
    <VizLayout
      toolbar={<NumberListInput initial={values} onSubmit={setValues} maxLength={7} label="Nodes" />}
      visual={
        <div className="linked-list">
          <div className="ll-slot">
            <span className="ll-none">None</span>
            <span className="ll-label">{labels[-1]?.join(' · ')}</span>
          </div>
          {n > 1 && <span className="ll-arrow">{frame.next[0] === null ? '←' : ''}</span>}

          {values.map((value, i) => (
            <div className="ll-group" key={i}>
              <div className="ll-slot">
                <div className={`ll-node ${frame.pointers.curr === i ? 'comparing' : frame.pointers.prev === i ? 'sorted' : ''}`}>
                  <span className="ll-val">{value}</span>
                  <span className="ll-next">{frame.next[i] === null ? '∅' : '•'}</span>
                </div>
                <span className="ll-label">{labels[i]?.join(' · ')}</span>
              </div>
              {i < n - 1 && <span className="ll-arrow">{connector(i)}</span>}
            </div>
          ))}

          <span className="ll-arrow">{frame.next[n - 1] === null ? '→' : ''}</span>
          <div className="ll-slot">
            <span className="ll-none">None</span>
            <span className="ll-label">{labels[n]?.join(' · ')}</span>
          </div>
        </div>
      }
      legend={[['comparing', 'curr'], ['sorted', 'prev (head of reversed part)']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default LinkedList
