
const express = require('express')
const cors = require('cors')
require('dotenv').config()

const app = express()
const PORT = process.env.PORT || 5001

app.use(cors({
  origin: 'http://localhost:5173',
}))

app.use(express.json())

app.get('/api/health', (req, res) => {
  res.json({
    success: true,
    message: 'Algorithm Visualizer API is running!',
  })
})

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`)
})

app.get('/api/algorithms', (req, res) => {
  const algorithms = [
    {
      name: 'Bubble Sort',
      bestTime: 'O(n)',
      averageTime: 'O(n²)',
      worstTime: 'O(n²)',
      space: 'O(1)',
      description:
        'Compares adjacent elements and swaps them when they are out of order.',
    },
    {
      name: 'Selection Sort',
      bestTime: 'O(n²)',
      averageTime: 'O(n²)',
      worstTime: 'O(n²)',
      space: 'O(1)',
      description:
        'Finds the smallest element in the unsorted section and moves it into position.',
    },
    {
      name: 'Insertion Sort',
      bestTime: 'O(n)',
      averageTime: 'O(n²)',
      worstTime: 'O(n²)',
      space: 'O(1)',
      description:
        'Inserts each element into its correct position in the sorted section.',
    },
  ]

  res.json({
    success: true,
    count: algorithms.length,
    algorithms,
  })
})
