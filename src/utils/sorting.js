export function bubbleSort(array) {
  const result = [...array]

  for (let i = 0; i < result.length; i++) {
    for (let j = 0; j < result.length - i - 1; j++) {
      if (result[j] > result[j + 1]) {
        const temp = result[j]
        result[j] = result[j + 1]
        result[j + 1] = temp
      }
    }
  }

  return result
}
export function selectionSort(array) {
  const result = [...array]

  for (let i = 0; i < result.length; i++) {
    let min = i

    for (let j = i + 1; j < result.length; j++) {
      if (result[j] < result[min]) {
        min = j
      }
    }

    const temp = result[i]
    result[i] = result[min]
    result[min] = temp
  }

  return result
}
export function insertionSort(array) {
  const result = [...array]

  for (let i = 1; i < result.length; i++) {
    const current = result[i]
    let j = i - 1

    while (j >= 0 && result[j] > current) {
      result[j + 1] = result[j]
      j--
    }

    result[j + 1] = current
  }

  return result
}

export function bubbleSortSteps(array) {
  const result = [...array]
  const steps = []

  steps.push({
    array: [...result],
    comparing: [],
    swapped: false,
  })

  for (let i = 0; i < result.length; i++) {
    for (let j = 0; j < result.length - i - 1; j++) {
      const comparing = [j, j + 1]
      let swapped = false

      if (result[j] > result[j + 1]) {
        const temp = result[j]
        result[j] = result[j + 1]
        result[j + 1] = temp
        swapped = true
      }

      steps.push({
        array: [...result],
        comparing,
        swapped,
      })
    }
  }

  return steps
}
