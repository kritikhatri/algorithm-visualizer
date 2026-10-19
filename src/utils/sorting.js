
function createStep(array, comparing = [], swapping = [], sorted = [], comparisons = 0, swaps = 0) {
  return {
    array: [...array],
    comparing: [...comparing],
    swapping: [...swapping],
    sorted: [...sorted],
    comparisons,
    swaps,
  }
}

export function bubbleSortSteps(array) {
  const values = [...array]
  const steps = [createStep(values)]
  let comparisons = 0
  let swaps = 0
  const sorted = []

  for (let i = 0; i < values.length; i++) {
    let changed = false

    for (let j = 0; j < values.length - i - 1; j++) {
      comparisons++

      if (values[j] > values[j + 1]) {
        steps.push(createStep(values, [j, j + 1], [], sorted, comparisons, swaps))

        ;[values[j], values[j + 1]] = [values[j + 1], values[j]]
        swaps++
        changed = true

        steps.push(createStep(values, [], [j, j + 1], sorted, comparisons, swaps))
      } else {
        steps.push(createStep(values, [j, j + 1], [], sorted, comparisons, swaps))
      }
    }

    sorted.unshift(values.length - i - 1)
    steps.push(createStep(values, [], [], sorted, comparisons, swaps))

    if (!changed) break
  }

  return steps
}

export function selectionSortSteps(array) {
  const values = [...array]
  const steps = [createStep(values)]
  let comparisons = 0
  let swaps = 0
  const sorted = []

  for (let i = 0; i < values.length - 1; i++) {
    let min = i

    for (let j = i + 1; j < values.length; j++) {
      comparisons++
      steps.push(createStep(values, [min, j], [], sorted, comparisons, swaps))

      if (values[j] < values[min]) min = j
    }

    if (min !== i) {
      ;[values[i], values[min]] = [values[min], values[i]]
      swaps++
      steps.push(createStep(values, [], [i, min], sorted, comparisons, swaps))
    }

    sorted.push(i)
    steps.push(createStep(values, [], [], sorted, comparisons, swaps))
  }

  if (values.length) sorted.push(values.length - 1)
  steps.push(createStep(values, [], [], sorted, comparisons, swaps))
  return steps
}

export function insertionSortSteps(array) {
  const values = [...array]
  const steps = [createStep(values)]
  let comparisons = 0
  let swaps = 0

  for (let i = 1; i < values.length; i++) {
    const key = values[i]
    let j = i - 1

    while (j >= 0) {
      comparisons++
      steps.push(createStep(values, [j, j + 1], [], [], comparisons, swaps))

      if (values[j] <= key) break

      values[j + 1] = values[j]
      swaps++
      steps.push(createStep(values, [], [j, j + 1], [], comparisons, swaps))
      j--
    }

    values[j + 1] = key
    steps.push(createStep(values, [], [], [], comparisons, swaps))
  }

  steps.push(createStep(values, [], [], values.map((_, i) => i), comparisons, swaps))
  return steps
}

export function mergeSortSteps(array) {
  const values = [...array]
  const steps = [createStep(values)]
  let comparisons = 0
  let swaps = 0

  function merge(left, mid, right) {
    const leftValues = values.slice(left, mid + 1)
    const rightValues = values.slice(mid + 1, right + 1)
    let i = 0
    let j = 0
    let k = left

    while (i < leftValues.length && j < rightValues.length) {
      comparisons++
      steps.push(createStep(values, [left + i, mid + 1 + j], [], [], comparisons, swaps))

      if (leftValues[i] <= rightValues[j]) {
        values[k] = leftValues[i]
        i++
      } else {
        values[k] = rightValues[j]
        j++
      }

      swaps++
      steps.push(createStep(values, [], [k], [], comparisons, swaps))
      k++
    }

    while (i < leftValues.length) {
      values[k] = leftValues[i]
      i++
      swaps++
      steps.push(createStep(values, [], [k], [], comparisons, swaps))
      k++
    }

    while (j < rightValues.length) {
      values[k] = rightValues[j]
      j++
      swaps++
      steps.push(createStep(values, [], [k], [], comparisons, swaps))
      k++
    }
  }

  function divide(left, right) {
    if (left >= right) return

    const mid = Math.floor((left + right) / 2)
    divide(left, mid)
    divide(mid + 1, right)
    merge(left, mid, right)
  }

  divide(0, values.length - 1)
  steps.push(createStep(values, [], [], values.map((_, i) => i), comparisons, swaps))
  return steps
}

export function quickSortSteps(array) {
  const values = [...array]
  const steps = [createStep(values)]
  let comparisons = 0
  let swaps = 0
  const sorted = []

  function swap(i, j) {
    if (i === j) return

    ;[values[i], values[j]] = [values[j], values[i]]
    swaps++
    steps.push(createStep(values, [], [i, j], sorted, comparisons, swaps))
  }

  function partition(low, high) {
    const pivot = values[high]
    let i = low

    for (let j = low; j < high; j++) {
      comparisons++
      steps.push(createStep(values, [j, high], [], sorted, comparisons, swaps))

      if (values[j] < pivot) {
        swap(i, j)
        i++
      }
    }

    swap(i, high)
    sorted.push(i)
    steps.push(createStep(values, [], [], sorted, comparisons, swaps))
    return i
  }

  function quickSort(low, high) {
    if (low > high) return

    if (low === high) {
      sorted.push(low)
      steps.push(createStep(values, [], [], sorted, comparisons, swaps))
      return
    }

    const pivotIndex = partition(low, high)
    quickSort(low, pivotIndex - 1)
    quickSort(pivotIndex + 1, high)
  }

  if (values.length) quickSort(0, values.length - 1)
  steps.push(createStep(values, [], [], values.map((_, i) => i), comparisons, swaps))
  return steps
}

// Keep these exports if other files already use them.
export function bubbleSort(array) {
  return bubbleSortSteps(array).at(-1).array
}

export function selectionSort(array) {
  return selectionSortSteps(array).at(-1).array
}

export function insertionSort(array) {
  return insertionSortSteps(array).at(-1).array
}

