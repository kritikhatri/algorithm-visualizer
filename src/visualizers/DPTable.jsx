import { useMemo, useState } from 'react'
import { PlayerControls, VizLayout, useStepPlayer } from './common'

const CODE = `def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]`

function lcsSteps(a, b) {
  const rows = a.length + 1
  const cols = b.length + 1
  const dp = Array.from({ length: rows }, (_, i) =>
    Array.from({ length: cols }, (_, j) => (i === 0 || j === 0 ? 0 : null))
  )
  const frames = []
  const push = (line, message, extra = {}) =>
    frames.push({ table: dp.map((row) => [...row]), line, message, ...extra })

  push(2, 'Row 0 and column 0 are 0: an empty string has no common subsequence.')

  for (let i = 1; i < rows; i++) {
    for (let j = 1; j < cols; j++) {
      const vars = { i, j, 'a[i-1]': a[i - 1], 'b[j-1]': b[j - 1] }
      const match = a[i - 1] === b[j - 1]
      push(5, `Compare a[${i - 1}] = '${a[i - 1]}' with b[${j - 1}] = '${b[j - 1]}': ${match ? 'match!' : 'different.'}`, {
        cell: [i, j],
        vars,
      })
      if (match) {
        dp[i][j] = dp[i - 1][j - 1] + 1
        push(6, `Match: take the diagonal ${dp[i - 1][j - 1]} + 1 = ${dp[i][j]}.`, {
          cell: [i, j], deps: [[i - 1, j - 1]], vars,
        })
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1])
        push(8, `No match: best of above (${dp[i - 1][j]}) and left (${dp[i][j - 1]}) = ${dp[i][j]}.`, {
          cell: [i, j], deps: [[i - 1, j], [i, j - 1]], vars,
        })
      }
    }
  }

  // Walk back from the bottom-right corner to recover one LCS.
  const path = []
  const letters = []
  let i = a.length
  let j = b.length
  while (i > 0 && j > 0) {
    path.push([i, j])
    if (a[i - 1] === b[j - 1]) {
      letters.unshift(a[i - 1])
      i--
      j--
    } else if (dp[i - 1][j] >= dp[i][j - 1]) {
      i--
    } else {
      j--
    }
  }
  const answer = dp[a.length][b.length]
  push(9, `The answer is dp[-1][-1] = ${answer}. Tracing back gives "${letters.join('')}".`, {
    path,
    vars: { result: answer, lcs: letters.join('') },
  })
  return frames
}

const has = (list, i, j) => list?.some(([r, c]) => r === i && c === j)

function DPTable() {
  const [a, setA] = useState('ABCBDAB')
  const [b, setB] = useState('BDCABA')
  const [draft, setDraft] = useState({ a, b })
  const [error, setError] = useState('')

  const frames = useMemo(() => lcsSteps(a, b), [a, b])
  const player = useStepPlayer(frames)
  const { frame } = player

  function handleSubmit(event) {
    event.preventDefault()
    const next = { a: draft.a.trim().toUpperCase(), b: draft.b.trim().toUpperCase() }
    if (![next.a, next.b].every((s) => /^[A-Z]{1,8}$/.test(s))) {
      setError('Use 1–8 letters for each string.')
      return
    }
    setError('')
    setA(next.a)
    setB(next.b)
  }

  const cellClass = (i, j) =>
    has(frame.path, i, j) && a[i - 1] === b[j - 1]
      ? 'found'
      : has(frame.path, i, j)
        ? 'pivot'
        : frame.cell?.[0] === i && frame.cell?.[1] === j
          ? 'swapping'
          : has(frame.deps, i, j)
            ? 'comparing'
            : ''

  return (
    <VizLayout
      toolbar={
        <form className="inline-form" onSubmit={handleSubmit}>
          <label><span>a</span><input value={draft.a} maxLength={8} onChange={(e) => setDraft({ ...draft, a: e.target.value })} /></label>
          <label><span>b</span><input value={draft.b} maxLength={8} onChange={(e) => setDraft({ ...draft, b: e.target.value })} /></label>
          <button className="button ghost small" type="submit">Load</button>
          {error && <span className="error-text">{error}</span>}
        </form>
      }
      visual={
        <div className="dp-wrap">
          <table className="dp-table">
            <thead>
              <tr>
                <th />
                <th className="muted">∅</th>
                {[...b].map((ch, j) => (
                  <th key={j} className={frame.cell?.[1] === j + 1 ? 'hl' : ''}>{ch}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {frame.table.map((row, i) => (
                <tr key={i}>
                  <th className={frame.cell?.[0] === i && i > 0 ? 'hl' : i === 0 ? 'muted' : ''}>{i === 0 ? '∅' : a[i - 1]}</th>
                  {row.map((value, j) => (
                    <td key={j} className={cellClass(i, j)}>{value ?? ''}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      }
      legend={[
        ['swapping', 'Filling'],
        ['comparing', 'Depends on'],
        ['found', 'Matched letter in LCS'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default DPTable
