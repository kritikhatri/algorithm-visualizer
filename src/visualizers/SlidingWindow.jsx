import { useMemo, useState } from 'react'
import { ArrayCells, PlayerControls, VizLayout } from './common'
import { useStepPlayer } from './helpers'

const CODE = `def longest_unique(s):
    seen = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in seen:
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best`

function windowSteps(s) {
  const chars = [...s]
  const frames = []
  const seen = new Set()
  let left = 0
  let best = 0
  let bestRange = null

  const push = (line, message, right, extra = {}) =>
    frames.push({
      array: chars,
      line,
      message,
      range: right === undefined ? null : [left, right],
      pointers: right === undefined ? {} : { left, right },
      vars: { left, ...(right !== undefined && { right }), best, seen: [...seen] },
      ...extra,
    })

  push(3, 'Start with an empty window.')
  chars.forEach((ch, right) => {
    push(4, `Move right to '${ch}' (index ${right}).`, right, { comparing: [right] })
    while (seen.has(ch)) {
      const duplicate = chars.indexOf(ch, left)
      push(5, `'${ch}' is already in the window. Shrink from the left.`, right, { comparing: [right], swapping: [duplicate] })
      seen.delete(chars[left])
      left++
      push(7, `Removed '${chars[left - 1]}'. Window is now indices ${left}–${right - 1}.`, right, { comparing: [right] })
    }
    seen.add(ch)
    if (right - left + 1 > best) {
      best = right - left + 1
      bestRange = [left, right]
      push(9, `New best! "${chars.slice(left, right + 1).join('')}" has length ${best}.`, right, { pivot: range(left, right) })
    } else {
      push(9, `Window "${chars.slice(left, right + 1).join('')}" (length ${right - left + 1}) isn't longer than ${best}.`, right)
    }
  })
  frames.push({
    array: chars,
    line: 10,
    message: chars.length
      ? `Longest substring without repeats: "${chars.slice(bestRange[0], bestRange[1] + 1).join('')}" (length ${best}).`
      : 'Empty string: the answer is 0.',
    found: bestRange ? range(...bestRange) : [],
    pointers: {},
    vars: { best },
  })
  return frames
}

function range(from, to) {
  return Array.from({ length: to - from + 1 }, (_, i) => from + i)
}

function SlidingWindow() {
  const [text, setText] = useState('abcabcbb')
  const [draft, setDraft] = useState(text)
  const [error, setError] = useState('')

  const frames = useMemo(() => windowSteps(text), [text])
  const player = useStepPlayer(frames)
  const { frame } = player

  function handleSubmit(event) {
    event.preventDefault()
    if (!/^[a-z]{1,14}$/i.test(draft.trim())) {
      setError('Use 1–14 letters.')
      return
    }
    setError('')
    setText(draft.trim().toLowerCase())
  }

  return (
    <VizLayout
      toolbar={
        <form className="inline-form" onSubmit={handleSubmit}>
          <label>
            <span>String</span>
            <input value={draft} maxLength={14} onChange={(event) => setDraft(event.target.value)} />
          </label>
          <button className="button ghost small" type="submit">Load</button>
          {['abcabcbb', 'pwwkew', 'dvdf'].map((sample) => (
            <button key={sample} type="button" className="button ghost small" onClick={() => { setDraft(sample); setText(sample) }}>
              {sample}
            </button>
          ))}
          {error && <span className="error-text">{error}</span>}
        </form>
      }
      visual={<ArrayCells frame={frame} />}
      legend={[
        ['comparing', 'right (new char)'],
        ['swapping', 'Duplicate'],
        ['pivot', 'New best window'],
        ['dim', 'Outside window'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default SlidingWindow
