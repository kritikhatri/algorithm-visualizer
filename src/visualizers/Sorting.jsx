import { useMemo, useState } from 'react'
import { sortingAlgorithms } from './sortingSteps'
import {
  ArrayBars,
  NumberListInput,
  PlayerControls,
  VizLayout,
  randomInts,
  useStepPlayer,
} from './common'

function Sorting() {
  const [algorithm, setAlgorithm] = useState('bubble')
  const [values, setValues] = useState([42, 17, 88, 23, 65, 9, 54, 31])
  const [inputKey, setInputKey] = useState(0)

  const { code, steps } = sortingAlgorithms[algorithm]
  const frames = useMemo(() => steps(values), [steps, values])
  const player = useStepPlayer(frames)
  const { frame } = player

  function randomize() {
    setValues(randomInts(8, 5, 99))
    setInputKey((key) => key + 1)
  }

  return (
    <VizLayout
      toolbar={
        <>
          <div className="tabs compact" role="group" aria-label="Algorithm">
            {Object.entries(sortingAlgorithms).map(([id, { name }]) => (
              <button
                key={id}
                className={`tab ${algorithm === id ? 'active' : ''}`}
                aria-pressed={algorithm === id}
                onClick={() => setAlgorithm(id)}
              >
                {name}
              </button>
            ))}
          </div>
          <NumberListInput key={inputKey} initial={values} onSubmit={setValues} maxLength={12} min={1} max={99} />
          <button className="button ghost small" onClick={randomize}>⚄ Random</button>
          <div className="stat-chips">
            <span>Comparisons <strong>{frame.comparisons}</strong></span>
            <span>Swaps / writes <strong>{frame.swaps}</strong></span>
          </div>
        </>
      }
      visual={<ArrayBars frame={frame} />}
      legend={[
        ['comparing', 'Comparing'],
        ['swapping', 'Swapping / writing'],
        ['pivot', 'Key / pivot / smallest'],
        ['sorted', 'Final position'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={code}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default Sorting
