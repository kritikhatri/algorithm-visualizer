
import { useEffect, useState } from 'react'
import './App.css'

import Header from './components/Header'
import ArrayControls from './components/ArrayControls'
import ArrayVisualizer from './components/ArrayVisualizer'
import AlgorithmSelector from './components/AlgorithmSelector'
import AlgorithmInfo from './components/AlgorithmInfo'
import Statistics from './components/Statistics'

import {
  bubbleSortSteps,
  selectionSortSteps,
  insertionSortSteps,
  mergeSortSteps,
  quickSortSteps,
} from './utils/sorting'

const algorithmFunctions = {
  bubble: bubbleSortSteps,
  selection: selectionSortSteps,
  insertion: insertionSortSteps,
  merge: mergeSortSteps,
  quick: quickSortSteps,
}

function App() {
  const [apiStatus, setApiStatus] = useState('Checking...')
  const [input, setInput] = useState('4, 2, 3')
  const [array, setArray] = useState([4, 2, 3])
  const [error, setError] = useState('')
  const [algorithm, setAlgorithm] = useState('bubble')

  const [animationSteps, setAnimationSteps] = useState([])
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [speed, setSpeed] = useState(600)

  const currentFrame = animationSteps[currentStep]

  useEffect(() => {
    fetch('/api/health')
      .then((response) => {
        if (!response.ok) throw new Error('Backend request failed')
        return response.json()
      })
      .then((data) => setApiStatus(data.message || 'Connected'))
      .catch(() => setApiStatus('Backend unavailable'))
  }, [])

  useEffect(() => {
    if (!isPlaying || animationSteps.length === 0) return

    if (currentStep >= animationSteps.length - 1) {
      setIsPlaying(false)
      return
    }

    const timer = setTimeout(() => {
      setCurrentStep((step) => step + 1)
    }, speed)

    return () => clearTimeout(timer)
  }, [isPlaying, currentStep, animationSteps, speed])

  useEffect(() => {
    if (currentFrame) {
      setArray(currentFrame.array)
    }
  }, [currentFrame])

  function stopAnimation() {
    setIsPlaying(false)
    setAnimationSteps([])
    setCurrentStep(0)
  }

  function handleSubmit(event) {
    event.preventDefault()

    const values = input.split(',').map((value) => value.trim())

    if (
      values.length < 1 ||
      values.length > 12 ||
      values.some(
        (value) =>
          value === '' ||
          !Number.isFinite(Number(value)) ||
          !Number.isInteger(Number(value))
      )
    ) {
      setError('Enter 1–12 whole numbers separated by commas.')
      return
    }

    stopAnimation()
    setArray(values.map(Number))
    setError('')
  }

  function handleGenerate() {
    const values = Array.from({ length: 8 }, () =>
      Math.floor(Math.random() * 90) + 10
    )

    stopAnimation()
    setArray(values)
    setInput(values.join(', '))
    setError('')
  }

  function handleReset() {
    stopAnimation()
    setArray([4, 2, 3])
    setInput('4, 2, 3')
    setError('')
  }

  
  function handleSort() {
    const createSteps = algorithmFunctions[algorithm]

    if (!createSteps || array.length === 0) {
      setError('Please enter an array before sorting.')
      return
    }

    const steps = createSteps(array)

    if (!steps || steps.length === 0) {
      setError('Could not generate sorting steps.')
      return
    }

    setError('')
    setAnimationSteps(steps)
    setCurrentStep(0)
    setIsPlaying(false)
    setArray(steps[0].array)
  }


  function handlePrevious() {
    setIsPlaying(false)
    setCurrentStep((step) => Math.max(0, step - 1))
  }

  function handleNext() {
    setIsPlaying(false)
    setCurrentStep((step) => Math.min(animationSteps.length - 1, step + 1))
  }

  function handleAlgorithmChange(value) {
    stopAnimation()
    setAlgorithm(value)
    setError('')
  }

  const hasAnimation = animationSteps.length > 0
  const isFinished = hasAnimation && currentStep === animationSteps.length - 1

  return (
    <main className="visualizer">
      <Header apiStatus={apiStatus} />

      <section className="control-panel">
        <AlgorithmSelector
          algorithm={algorithm}
          setAlgorithm={handleAlgorithmChange}
        />

        <ArrayControls
          input={input}
          setInput={setInput}
          onSubmit={handleSubmit}
          onGenerate={handleGenerate}
          onReset={handleReset}
        />

        <button
          className="sort-button primary-button"
          onClick={handleSort}
        >
          <span>▶</span> Start Sorting
        </button>
      </section>

      {error && <p className="error">{error}</p>}

      <section className="chart-panel">
        <div className="section-heading">
          <div>
            <h2>Array Visualization</h2>
            <p>Watch how the algorithm sorts your numbers.</p>
          </div>

          {hasAnimation && (
            <span className="step-count">
              Step {currentStep + 1} / {animationSteps.length}
            </span>
          )}
        </div>

        <ArrayVisualizer
          array={array}
          comparing={currentFrame?.comparing || []}
          swapping={currentFrame?.swapping || []}
          sorted={currentFrame?.sorted || []}
        />

        <div className="legend">
          <span><i className="legend-dot comparing-dot" /> Comparing</span>
          <span><i className="legend-dot swapping-dot" /> Swapping / moving</span>
          <span><i className="legend-dot sorted-dot" /> Sorted</span>
        </div>
      </section>

      <section className="playback-panel">
        <div className="playback-buttons">
          <button
          onClick={() => {
            if (!hasAnimation) {
              const createSteps = algorithmFunctions[algorithm]
              const steps = createSteps(array)
              if (!steps || steps.length === 0) {
                setError('Could not generate sorting steps.')
                return
              }
              setError('')
              setAnimationSteps(steps)
              setCurrentStep(0)
              setArray(steps[0].array)
              setIsPlaying(true)
              } else if (isFinished) {
                setCurrentStep(0)
                setIsPlaying(true)
              } else {
                setIsPlaying((playing) => !playing)
              }
            }}
          >
            ← Previous
          </button>

          <button
            className="play-button"
            onClick={() => {
              if (!hasAnimation) {
                handleSort()
              } else if (isFinished) {
                setCurrentStep(0)
                setIsPlaying(true)
              } else {
                setIsPlaying((playing) => !playing)
              }
            }}
          >
            {!hasAnimation
              ? '▶ Play'
              : isFinished
                ? '↻ Replay'
                : isPlaying
                  ? 'Ⅱ Pause'
                  : '▶ Resume'}
          </button>

          <button
            onClick={handleNext}
            disabled={!hasAnimation || isFinished}
          >
            Next →
          </button>
        </div>

        <div className="speed-control">
          <label htmlFor="speed">
            Animation speed
            <strong>
              {speed <= 200 ? ' Fast' : speed <= 500 ? ' Normal' : ' Slow'}
            </strong>
          </label>

          <input
            id="speed"
            type="range"
            min="100"
            max="1000"
            step="100"
            value={speed}
            onChange={(event) => setSpeed(Number(event.target.value))}
          />

          <div className="speed-labels">
            <span>Fast</span>
            <span>Slow</span>
          </div>
        </div>
      </section>

      <section className="live-stats">
        <article className="live-stat-card">
          <span className="stat-icon">⌕</span>
          <span className="stat-label">Comparisons</span>
          <strong>{currentFrame?.comparisons ?? 0}</strong>
        </article>

        <article className="live-stat-card">
          <span className="stat-icon">⇄</span>
          <span className="stat-label">Swaps / moves</span>
          <strong>{currentFrame?.swaps ?? 0}</strong>
        </article>

        <article className="live-stat-card">
          <span className="stat-icon">▦</span>
          <span className="stat-label">Array size</span>
          <strong>{array.length}</strong>
        </article>
      </section>

      <Statistics array={array} />
      <AlgorithmInfo algorithm={algorithm} />
    </main>
  )
}

export default App
