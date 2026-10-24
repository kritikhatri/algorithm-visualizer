import { useState } from 'react'
import { pyRepr } from '../utils/format'
import { VizLayout, raw } from './common'

const CODE = `from collections import deque

stack = []
queue = deque()

stack.append(x)     # push: O(1)
stack.pop()         # pop: O(1)
stack[-1]           # peek at the top

queue.append(x)     # enqueue: O(1)
queue.popleft()     # dequeue: O(1)
queue[0]            # peek at the front`

const LIMIT = 8

function StackQueue() {
  const [stack, setStack] = useState([3, 8])
  const [queue, setQueue] = useState([5, 1])
  const [nextValue, setNextValue] = useState(10)
  const [last, setLast] = useState({ line: null, message: 'Push and pop to compare LIFO with FIFO.' })

  function add(kind) {
    const list = kind === 'stack' ? stack : queue
    if (list.length >= LIMIT) {
      setLast({ line: null, message: `Let's keep it to ${LIMIT} items so it fits on screen.` })
      return
    }
    const value = nextValue
    setNextValue((v) => v + 1)
    if (kind === 'stack') {
      setStack([...stack, value])
      setLast({ line: 6, message: `push(${value}): it goes on top. The newest item is always the next out.` })
    } else {
      setQueue([...queue, value])
      setLast({ line: 10, message: `enqueue(${value}): it joins the back of the line.` })
    }
  }

  function remove(kind) {
    if (kind === 'stack') {
      if (!stack.length) return setLast({ line: 7, message: 'IndexError: pop from empty list' })
      setStack(stack.slice(0, -1))
      setLast({ line: 7, message: `pop() → ${stack.at(-1)}: last in, first out.` })
    } else {
      if (!queue.length) return setLast({ line: 11, message: 'IndexError: pop from an empty deque' })
      setQueue(queue.slice(1))
      setLast({ line: 11, message: `popleft() → ${queue[0]}: first in, first out.` })
    }
  }

  function peek(kind) {
    const list = kind === 'stack' ? stack : queue
    const value = kind === 'stack' ? list.at(-1) : list[0]
    setLast({
      line: kind === 'stack' ? 8 : 12,
      message: list.length ? `Peek → ${value} (nothing is removed).` : 'IndexError: the structure is empty.',
    })
  }

  return (
    <VizLayout
      toolbar={<span className="muted">Next value to add: <strong>{nextValue}</strong></span>}
      visual={
        <div className="sq-grid">
          <section className="sq-panel">
            <h3>Stack <span className="muted">(LIFO)</span></h3>
            <div className="stack-view">
              {stack.length === 0 && <span className="muted">empty</span>}
              {[...stack].reverse().map((value, i) => (
                <div className={`sq-item ${i === 0 ? 'top' : ''}`} key={`${value}-${stack.length - i}`}>
                  {value}
                  {i === 0 && <span className="sq-tag">top</span>}
                </div>
              ))}
            </div>
            <div className="sq-actions">
              <button className="button primary small" onClick={() => add('stack')}>push</button>
              <button className="button ghost small" onClick={() => remove('stack')}>pop</button>
              <button className="button ghost small" onClick={() => peek('stack')}>peek</button>
            </div>
          </section>

          <section className="sq-panel">
            <h3>Queue <span className="muted">(FIFO)</span></h3>
            <div className="queue-view">
              {queue.length === 0 && <span className="muted">empty</span>}
              {queue.map((value, i) => (
                <div className={`sq-item ${i === 0 ? 'front' : ''}`} key={`${value}-${i}`}>
                  {value}
                  {i === 0 && <span className="sq-tag">front</span>}
                </div>
              ))}
            </div>
            <div className="sq-actions">
              <button className="button primary small" onClick={() => add('queue')}>enqueue</button>
              <button className="button ghost small" onClick={() => remove('queue')}>dequeue</button>
              <button className="button ghost small" onClick={() => peek('queue')}>peek</button>
            </div>
          </section>
        </div>
      }
      message={last.message}
      code={CODE}
      line={last.line}
      vars={{ stack, queue: raw(`deque(${pyRepr(queue)})`) }}
    />
  )
}

export default StackQueue
