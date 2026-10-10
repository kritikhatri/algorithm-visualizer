
function generateBubbleSortSteps(originalArray) {
  const array = [...originalArray]
  const steps = []

  for (let i = 0; i < array.length - 1; i++) {
    for (let j = 0; j < array.length - 1 - i; j++) {
      steps.push({
        type: "compare",
        indices: [j, j + 1],
        array: [...array],
      })

      if (array[j] > array[j + 1]) {
        const temp = array[j]
        array[j] = array[j + 1]
        array[j + 1] = temp

        steps.push({
          type: "swap",
          indices: [j, j + 1],
          array: [...array],
        })
      }
    }
  }

  steps.push({
    type: "done",
    indices: [],
    array: [...array],
  })

  return steps
}

function App() {
  const steps = generateBubbleSortSteps([4, 2, 3])

  return (
    <div>
      <h1>Algorithm Visualizer</h1>
      <h2>Bubble Sort</h2>

      <p>Total recorded steps: {steps.length}</p>

      <h3>Recorded Steps</h3>

      {steps.map((step, index) => (
        <div key={index}>
          <strong>Step {index + 1}: {step.type}</strong>
          <p>Indices: {step.indices.join(", ") || "None"}</p>
          <p>Array: [{step.array.join(", ")}]</p>
        </div>
      ))}
    </div>
  )
}

export default App