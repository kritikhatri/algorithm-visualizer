import { useMemo, useState } from 'react'
import { PlayerControls, VizLayout } from './common'
import { useStepPlayer } from './helpers'

const CODE = `a & b    # AND: 1 only if both bits are 1
a | b    # OR: 1 if either bit is 1
a ^ b    # XOR: 1 if the bits differ
a << k   # shift left: multiply by 2**k
a >> k   # shift right: floor-divide by 2**k`

const BITS = 8

const OPS = {
  and: { label: 'a & b', line: 1, apply: (a, b) => a & b, rule: (x, y) => `${x} & ${y} = ${x & y}` },
  or: { label: 'a | b', line: 2, apply: (a, b) => a | b, rule: (x, y) => `${x} | ${y} = ${x | y}` },
  xor: { label: 'a ^ b', line: 3, apply: (a, b) => a ^ b, rule: (x, y) => `${x} ^ ${y} = ${x ^ y}` },
  shl: { label: 'a << k', line: 4, apply: (a, k) => (a << k) & 0xff },
  shr: { label: 'a >> k', line: 5, apply: (a, k) => a >> k },
}

const toBits = (n) => Array.from({ length: BITS }, (_, i) => (n >> (BITS - 1 - i)) & 1)

function bitSteps(op, a, b) {
  const { line, apply, rule } = OPS[op]
  const result = apply(a, b)
  const frames = []

  if (!rule) {
    const direction = op === 'shl' ? 'left' : 'right'
    frames.push({ result: null, line, message: `Shift every bit of ${a} ${direction} by ${b} place(s).`, vars: { a, k: b } })
    frames.push({
      result,
      line,
      message: op === 'shl'
        ? `${a} << ${b} = ${a} × 2^${b} = ${result}${a << b > 255 ? ' (bits beyond 8 drop off in this 8-bit view)' : ''}.`
        : `${a} >> ${b} = ${a} // 2^${b} = ${result}. Bits shifted past the right edge are lost.`,
      vars: { a, k: b, result },
    })
    return frames
  }

  frames.push({ result: null, line, message: 'Combine the two numbers one bit position at a time, from the right.', vars: { a, b } })
  let partial = 0
  for (let i = 0; i < BITS; i++) {
    const x = (a >> i) & 1
    const y = (b >> i) & 1
    partial |= (apply(x, y) & 1) << i
    frames.push({
      result: partial,
      upTo: i,
      active: i,
      line,
      message: `Bit ${i} (worth ${2 ** i}): ${rule(x, y)}`,
      vars: { a, b, 'result so far': partial },
    })
  }
  frames.push({ result, line, message: `${a} ${OPS[op].label.slice(2, -2)} ${b} = ${result}`, vars: { a, b, result } })
  return frames
}

function BitRow({ label, value, active, revealedFrom }) {
  const bits = value === null ? Array(BITS).fill(null) : toBits(value)
  return (
    <div className="bit-row">
      <span className="bit-label">{label}</span>
      {bits.map((bit, index) => {
        const position = BITS - 1 - index
        const hidden = revealedFrom !== undefined && position > revealedFrom
        return (
          <span
            key={index}
            className={`bit ${bit === 1 && !hidden ? 'on' : ''} ${position === active ? 'comparing' : ''}`}
          >
            {bit === null || hidden ? '' : bit}
          </span>
        )
      })}
      <span className="bit-value">{value === null ? '' : value}</span>
    </div>
  )
}

function Bits() {
  const [op, setOp] = useState('xor')
  const [a, setA] = useState(12)
  const [b, setB] = useState(10)

  const isShift = op === 'shl' || op === 'shr'
  const second = isShift ? Math.min(b, 7) : b
  const frames = useMemo(() => bitSteps(op, a, second), [op, a, second])
  const player = useStepPlayer(frames)
  const { frame } = player

  const clamp = (value, max) => Math.max(0, Math.min(max, Number(value) || 0))

  return (
    <VizLayout
      toolbar={
        <>
          <div className="tabs compact" role="group" aria-label="Operator">
            {Object.entries(OPS).map(([id, { label }]) => (
              <button key={id} className={`tab ${op === id ? 'active' : ''}`} aria-pressed={op === id} onClick={() => setOp(id)}>
                {label}
              </button>
            ))}
          </div>
          <label className="inline-field">
            <span>a</span>
            <input type="number" min="0" max="255" value={a} onChange={(e) => setA(clamp(e.target.value, 255))} />
          </label>
          <label className="inline-field">
            <span>{isShift ? 'k' : 'b'}</span>
            <input type="number" min="0" max={isShift ? 7 : 255} value={second} onChange={(e) => setB(clamp(e.target.value, isShift ? 7 : 255))} />
          </label>
        </>
      }
      visual={
        <div className="bits">
          <div className="bit-row header">
            <span className="bit-label" />
            {Array.from({ length: BITS }, (_, i) => <span key={i} className="bit-weight">{2 ** (BITS - 1 - i)}</span>)}
            <span className="bit-value" />
          </div>
          <BitRow label="a" value={a} active={frame.active} />
          {!isShift && <BitRow label="b" value={b} active={frame.active} />}
          <div className="bit-divider" />
          <BitRow label={OPS[op].label} value={frame.result} active={frame.active} revealedFrom={frame.upTo} />
        </div>
      }
      legend={[['comparing', 'Current bit'], ['found', 'Bit is 1']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default Bits
