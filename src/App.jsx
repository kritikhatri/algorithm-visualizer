
import { useEffect, useState } from 'react'
import './App.css'
import Header from './components/Header'
import ArrayControls from './components/ArrayControls'
import ArrayVisualizer from './components/ArrayVisualizer'
import AlgorithmSelector from './components/AlgorithmSelector'
import SortButton from './components/SortButton'
import { bubbleSort, selectionSort, insertionSort } from './utils/sorting'
import AlgorithmInfo from './components/AlgorithmInfo'

function App() {
  const [apiStatus, setApiStatus] = useState('Checking...')
  const [input, setInput] = useState('4, 2, 3')
  const [array, setArray] = useState([4, 2, 3])
  const [error, setError] = useState('')
  const [algorithm, setAlgorithm] = useState('bubble')
  const [isSorting, setIsSorting] = useState(false) 
  const handleSort = () => {
  if (algorithm === 'bubble') {
    setArray(bubbleSort(array))
  } else if (algorithm === 'selection') {
    setArray(selectionSort(array))
  } else if (algorithm === 'insertion') {
  setArray(insertionSort(array))
  }
}

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
  setError('')
}

function handleGenerate() {
  const values = Array.from({ length: 8 }, () =>
    Math.floor(Math.random() * 90) + 10
  )

  setArray(values)
  setInput(values.join(', '))
  setError('')
}

function handleReset() {
  setArray([4, 2, 3])
  setInput('4, 2, 3')
  setError('')
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
      <ArrayVisualizer array={array} />
      <AlgorithmInfo algorithm={algorithm} />
      <SortButton onSort={handleSort} isSorting={isSorting} />
      
    </main>

  )
}

export default App
