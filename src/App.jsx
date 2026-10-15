
import { useEffect, useState } from 'react'
import './App.css'

function generateSteps(originalArray, algorithm) {
  const array = [...originalArray]
  const steps = []

  function record(type, indices = []) {
    steps.push({
      type,
      indices,
      array: [...array],
    })
  }

  record('start')

  if (algorithm === 'Bubble Sort') {
    for (let i = 0; i < array.length - 1; i++) {
      for (let j = 0; j < array.length - 1 - i; j++) {
        record('compare', [j, j + 1])

        if (array[j] > array[j + 1]) {
          ;[array[j], array[j + 1]] = [array[j + 1], array[j]]
          record('swap', [j, j + 1])
        }
      }
    }
  } else if (algorithm === 'Selection Sort') {
    for (let i = 0; i < array.length - 1; i++) {
      let minIndex = i

      for (let j = i + 1; j < array.length; j++) {
        record('compare', [minIndex, j])

        if (array[j] < array[minIndex]) {
          minIndex = j
          record('new minimum', [i, minIndex])
        }
      }

      if (minIndex !== i) {
        ;[array[i], array[minIndex]] = [array[minIndex], array[i]]
        record('swap', [i, minIndex])
      }
    }
  } else if (algorithm === 'Insertion Sort') {
    for (let i = 1; i < array.length; i++) {
      const current = array[i]
      let j = i - 1

      record('select', [i])

      while (j >= 0 && array[j] > current) {
        record('compare', [j, j + 1])
        array[j + 1] = array[j]
        record('shift', [j, j + 1])
        j--
      }

      array[j + 1] = current
      record('insert', [j + 1])
    }
  }

  record('done')
  return steps
}

function App() {
  const [input, setInput] = useState('4, 2, 3')
  const [array, setArray] = useState([4, 2, 3])
  const [algorithm, setAlgorithm] = useState('Bubble Sort')
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [error, setError] = useState('')

  const steps = generateSteps(array, algorithm)
  const step = steps[currentStep]

  useEffect(() => {
    if (!isPlaying) return

    const timer = setInterval(() => {
      setCurrentStep((previousStep) => {
        if (previousStep >= steps.length - 1) {
          setIsPlaying(false)
          return previousStep
        }

        return previousStep + 1
      })
    }, 800)

    return () => clearInterval(timer)
  }, [isPlaying, steps.length])

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

    setIsPlaying(false)
    setArray(values.map(Number))
    setCurrentStep(0)
    setError('')
  }

  function handleAlgorithmChange(event) {
    setAlgorithm(event.target.value)
    setIsPlaying(false)
    setCurrentStep(0)
  }

  function handleNext() {
    setIsPlaying(false)
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  function handlePrevious() {
    setIsPlaying(false)
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  function handleReset() {
    setIsPlaying(false)
    setCurrentStep(0)
  }

  return (
    <main className="visualizer">
      <header className="page-header">
        <p className="eyebrow">LEARN • VISUALIZE • UNDERSTAND</p>
        <h1>Algorithm Visualizer</h1>
        <p className="subtitle">
          Watch sorting algorithms come to life, one step at a time.
        </p>
      </header>

      <section className="panel">
        <form className="input-section" onSubmit={handleSubmit}>
          <label htmlFor="array-input">Your array</label>

          <div className="input-row">
            <input
              id="array-input"
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="e.g. 8, 3, 6, 1, 5"
            />
            <button className="primary-button" type="submit">
              Visualize
            </button>
          </div>

          <p className="helper-text">
            Enter up to 12 whole numbers separated by commas.
          </p>

          {error && <p className="error-message">{error}</p>}
        </form>

        <div className="algorithm-selector">
          <label htmlFor="algorithm">Choose algorithm</label>
          <select
            id="algorithm"
            value={algorithm}
            onChange={handleAlgorithmChange}
          >
            <option>Bubble Sort</option>
            <option>Selection Sort</option>
            <option>Insertion Sort</option>
          </select>
        </div>

        <div className="section-heading">
          <div>
            <p className="eyebrow">CURRENT ALGORITHM</p>
            <h2>{algorithm}</h2>
          </div>
          <span className="step-badge">
            Step {currentStep + 1} / {steps.length}
          </span>
        </div>

        <div className="array-container">
          {step.array.map((value, index) => {
            const isCompared = step.indices.includes(index)

            return (
              <div className="bar-wrapper" key={index}>
                <div
                  className={`bar ${isCompared ? 'highlight' : ''} ${
                    step.type === 'done' ? 'sorted' : ''
                  }`}
                  style={{
                    height: `${Math.max(
                      35,
                      Math.min(220, Math.abs(value) * 18 + 35)
                    )}px`,
                  }}
                >
                  <span>{value}</span>
                </div>
                <span className="index-label">Index {index}</span>
              </div>
            )
          })}
        </div>

        <div className="step-info">
          <span className={`action-label action-${step.type.replace(' ', '-')}`}>
            {step.type === 'done' ? '✓ Sorting complete' : `Action: ${step.type}`}
          </span>

          <p className="array-readout">
            Array: [{step.array.join(', ')}]
          </p>

          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: `${((currentStep + 1) / steps.length) * 100}%`,
              }}
            />
          </div>
        </div>

        <div className="controls">
          <button
            className="secondary-button"
            onClick={handlePrevious}
            disabled={currentStep === 0}
          >
            ← Previous
          </button>

          <button
            className="primary-button play-button"
            onClick={() => {
              if (currentStep === steps.length - 1) {
                setCurrentStep(0)
                setIsPlaying(true)
              } else {
                setIsPlaying(!isPlaying)
              }
            }}
          >
            {isPlaying ? 'Ⅱ Pause' : '▶ Play'}
          </button>

          <button className="secondary-button" onClick={handleReset}>
            ↺ Reset
          </button>

          <button
            className="secondary-button"
            onClick={handleNext}
            disabled={currentStep === steps.length - 1}
          >
            Next →
          </button>
        </div>
      </section>

      <footer className="page-footer">
        <p>Made with curiosity and a little bit of pink ✿</p>
      </footer>
    </main>
  )
}

export default App
