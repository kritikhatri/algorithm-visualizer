
import { useEffect, useState } from 'react'
import './App.css'

import Header from './components/Header'
import ArrayControls from './components/ArrayControls'
import ArrayVisualizer from './components/ArrayVisualizer'
import AlgorithmSelector from './components/AlgorithmSelector'
import SortButton from './components/SortButton'
import AlgorithmInfo from './components/AlgorithmInfo'
import Statistics from './components/Statistics'

import {
  bubbleSort,
  selectionSort,
  insertionSort,
  bubbleSortSteps,
} from './utils/sorting'

function App() {
  const [apiStatus, setApiStatus] = useState('Checking...')

  const [input, setInput] = useState('4, 2, 3')
  const [array, setArray] = useState([4, 2, 3])
  const [error, setError] = useState('')

  const [algorithm, setAlgorithm] = useState('bubble')
  const [isSorting, setIsSorting] = useState(false)

  const [animationSteps, setAnimationSteps] = useState([])
  const [currentStep, setCurrentStep] = useState(0)

  useEffect(() => {
    fetch('/api/health')
      .then((response) => response.json())
      .then((data) => setApiStatus(data.message))
      .catch(() => setApiStatus('Backend unavailable'))
  }, [])

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

    setArray(values.map(Number))
    setAnimationSteps([])
    setCurrentStep(0)
    setError('')
  }

  function handleGenerate() {
    const values = Array.from({ length: 8 }, () =>
      Math.floor(Math.random() * 90) + 10
    )

    setArray(values)
    setInput(values.join(', '))
    setAnimationSteps([])
    setCurrentStep(0)
    setError('')
  }

  function handleReset() {
    setArray([4, 2, 3])
    setInput('4, 2, 3')
    setAnimationSteps([])
    setCurrentStep(0)
    setIsSorting(false)
    setError('')
  }

  function handleSort() {
    setError('')

    if (algorithm === 'bubble') {
      const steps = bubbleSortSteps(array)

      setAnimationSteps(steps)
      setCurrentStep(0)
      setArray(steps[0].array)
    } else if (algorithm === 'selection') {
      setArray(selectionSort(array))
      setAnimationSteps([])
      setCurrentStep(0)
    } else if (algorithm === 'insertion') {
      setArray(insertionSort(array))
      setAnimationSteps([])
      setCurrentStep(0)
    }
  }

  function handleNextStep() {
    if (currentStep < animationSteps.length - 1) {
      const nextStep = currentStep + 1

      setCurrentStep(nextStep)
      setArray(animationSteps[nextStep].array)
    }
  }

  return (
    <main className="visualizer">
      <Header apiStatus={apiStatus} />

      <AlgorithmSelector
        algorithm={algorithm}
        setAlgorithm={setAlgorithm}
      />

      <p>Selected: {algorithm}</p>

      <ArrayControls
        input={input}
        setInput={setInput}
        onSubmit={handleSubmit}
        onGenerate={handleGenerate}
        onReset={handleReset}
      />

      {error && <p className="error">{error}</p>}

      <ArrayVisualizer array={array} />

      {algorithm === 'bubble' && animationSteps.length > 0 && (
        <section className="panel">
          <p>
            Step: {currentStep} of {animationSteps.length - 1}
          </p>

          <button
            onClick={handleNextStep}
            disabled={currentStep >= animationSteps.length - 1}
          >
            {currentStep >= animationSteps.length - 1
              ? 'Sorting Complete'
              : 'Next Step'}
          </button>
        </section>
      )}

      <Statistics array={array} />

      <AlgorithmInfo algorithm={algorithm} />

      <SortButton
        onSort={handleSort}
        isSorting={isSorting}
      />
    </main>
  )
}

export default App
