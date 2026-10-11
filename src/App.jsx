
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
  const [currentStep, setCurrentStep] = useState(0)

  const step = steps[currentStep]

  function handleNext() {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  function handlePrevious() {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  return (
    <div className="visualizer">
      <h1>Algorithm Visualizer</h1>
      <p className="subtitle">Learn Bubble Sort, one step at a time.</p>

      <div className="array-container">
        {step.array.map((value, index) => {
          const isCompared = step.indices.includes(index)

          return (
            <div className="bar-wrapper" key={index}>
              <div
                className={`bar ${isCompared ? "highlight" : ""}`}
                style={{ height: `${value * 35}px` }}
              >
                {value}
              </div>
              <span>Index {index}</span>
            </div>
          )
        })}
      </div>

      <div className="step-info">
        <h2>Action: {step.type}</h2>
        <p>Step {currentStep + 1} of {steps.length}</p>
        <p>Array: [{step.array.join(", ")}]</p>
      </div>

      <div className="controls">
        <button onClick={handlePrevious} disabled={currentStep === 0}>
          ← Previous
        </button>
        <button
          onClick={handleNext}
          disabled={currentStep === steps.length - 1}
        >
          Next →
        </button>
      </div>
    </div>
  )
}

export default App