// Step generators for the sorting visualizer. Each frame records the Python line
// that is running (`line`, 1-based in the matching `code`) and the live variables.

function recorder(values) {
  const frames = []
  const sorted = new Set()
  const stats = { comparisons: 0, swaps: 0 }

  function push(line, message, extra = {}) {
    frames.push({
      array: [...values],
      sorted: [...sorted],
      comparisons: stats.comparisons,
      swaps: stats.swaps,
      line,
      message,
      ...extra,
    })
  }

  function finish(line) {
    values.forEach((_, i) => sorted.add(i))
    push(line, `Done! Sorted with ${stats.comparisons} comparisons and ${stats.swaps} swaps/writes.`)
    return frames
  }

  return { push, finish, sorted, stats }
}

const BUBBLE = `def bubble_sort(nums):
    n = len(nums)
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
                swapped = True
        if not swapped:
            break
    return nums`

function bubbleSteps(input) {
  const a = [...input]
  const n = a.length
  const { push, finish, sorted, stats } = recorder(a)
  push(2, `Start with ${n} items.`, { vars: { n } })

  for (let i = 0; i < n; i++) {
    let swapped = false
    for (let j = 0; j < n - i - 1; j++) {
      stats.comparisons++
      push(6, `Compare ${a[j]} and ${a[j + 1]}.`, { comparing: [j, j + 1], vars: { n, i, j, swapped } })
      if (a[j] > a[j + 1]) {
        ;[a[j], a[j + 1]] = [a[j + 1], a[j]]
        stats.swaps++
        swapped = true
        push(7, `${a[j + 1]} is bigger, so it moves right.`, { swapping: [j, j + 1], vars: { n, i, j, swapped } })
      }
    }
    sorted.add(n - i - 1)
    push(9, `Pass ${i + 1} done: ${a[n - i - 1]} is in its final place.`, { vars: { n, i, swapped } })
    if (!swapped) {
      push(10, 'No swaps in this pass, so everything is sorted. Stop early.', { vars: { n, i, swapped } })
      break
    }
  }
  return finish(11)
}

const SELECTION = `def selection_sort(nums):
    n = len(nums)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            if nums[j] < nums[smallest]:
                smallest = j
        nums[i], nums[smallest] = nums[smallest], nums[i]
    return nums`

function selectionSteps(input) {
  const a = [...input]
  const n = a.length
  const { push, finish, sorted, stats } = recorder(a)
  push(2, `Start with ${n} items.`, { vars: { n } })

  for (let i = 0; i < n - 1; i++) {
    let smallest = i
    push(4, `Assume ${a[i]} (index ${i}) is the smallest so far.`, { pivot: [i], vars: { i, smallest } })
    for (let j = i + 1; j < n; j++) {
      stats.comparisons++
      push(6, `Is ${a[j]} smaller than ${a[smallest]}?`, { comparing: [j], pivot: [smallest], vars: { i, j, smallest } })
      if (a[j] < a[smallest]) {
        smallest = j
        push(7, `Yes, ${a[j]} is the new smallest.`, { pivot: [smallest], vars: { i, j, smallest } })
      }
    }
    if (smallest !== i) {
      ;[a[i], a[smallest]] = [a[smallest], a[i]]
      stats.swaps++
    }
    sorted.add(i)
    push(8, smallest !== i ? `Swap ${a[i]} into index ${i}.` : `${a[i]} is already in place.`, {
      swapping: [i, smallest],
      vars: { i, smallest },
    })
  }
  return finish(9)
}

const INSERTION = `def insertion_sort(nums):
    for i in range(1, len(nums)):
        key = nums[i]
        j = i - 1
        while j >= 0 and nums[j] > key:
            nums[j + 1] = nums[j]
            j -= 1
        nums[j + 1] = key
    return nums`

function insertionSteps(input) {
  const a = [...input]
  const { push, finish, stats } = recorder(a)
  push(2, 'The first item on its own is a sorted prefix.', { vars: {} })

  for (let i = 1; i < a.length; i++) {
    const key = a[i]
    let j = i - 1
    push(3, `Take key = ${key} from index ${i}.`, { pivot: [i], vars: { i, key } })
    while (j >= 0) {
      stats.comparisons++
      push(5, `Is ${a[j]} > key (${key})?`, { comparing: [j], vars: { i, j, key } })
      if (a[j] <= key) break
      a[j + 1] = a[j]
      stats.swaps++
      push(6, `Yes, shift ${a[j]} one place right.`, { swapping: [j + 1], vars: { i, j, key } })
      j--
    }
    a[j + 1] = key
    push(8, `Drop key ${key} into index ${j + 1}.`, { swapping: [j + 1], vars: { i, j, key } })
  }
  return finish(9)
}

const MERGE = `def merge_sort(nums, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo >= hi:
        return nums
    mid = (lo + hi) // 2
    merge_sort(nums, lo, mid)
    merge_sort(nums, mid + 1, hi)
    left, right = nums[lo:mid + 1], nums[mid + 1:hi + 1]
    i = j = 0
    for k in range(lo, hi + 1):
        if j >= len(right) or (i < len(left) and left[i] <= right[j]):
            nums[k] = left[i]
            i += 1
        else:
            nums[k] = right[j]
            j += 1
    return nums`

function mergeSteps(input) {
  const a = [...input]
  const { push, finish, stats } = recorder(a)

  function sort(lo, hi) {
    if (lo >= hi) return
    const mid = Math.floor((lo + hi) / 2)
    push(6, `Split indices ${lo}–${hi} at mid = ${mid}.`, { range: [lo, hi], vars: { lo, mid, hi } })
    sort(lo, mid)
    sort(mid + 1, hi)

    const left = a.slice(lo, mid + 1)
    const right = a.slice(mid + 1, hi + 1)
    push(9, `Both halves are sorted. Merge them.`, { range: [lo, hi], vars: { lo, mid, hi, left, right } })

    let i = 0
    let j = 0
    for (let k = lo; k <= hi; k++) {
      const both = i < left.length && j < right.length
      if (both) stats.comparisons++
      const takeLeft = j >= right.length || (i < left.length && left[i] <= right[j])
      a[k] = takeLeft ? left[i++] : right[j++]
      stats.swaps++
      push(takeLeft ? 13 : 16, both
        ? `${a[k]} is the smaller head, so write it to index ${k}.`
        : `Copy the remaining ${a[k]} to index ${k}.`, {
        range: [lo, hi],
        swapping: [k],
        vars: { k, i, j, left, right },
      })
    }
  }

  push(3, `Start with ${a.length} items.`, { vars: { lo: 0, hi: a.length - 1 } })
  sort(0, a.length - 1)
  return finish(18)
}

const QUICK = `def quick_sort(nums, lo=0, hi=None):
    if hi is None:
        hi = len(nums) - 1
    if lo < hi:
        p = partition(nums, lo, hi)
        quick_sort(nums, lo, p - 1)
        quick_sort(nums, p + 1, hi)
    return nums

def partition(nums, lo, hi):
    pivot = nums[hi]
    i = lo
    for j in range(lo, hi):
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[hi] = nums[hi], nums[i]
    return i`

function quickSteps(input) {
  const a = [...input]
  const { push, finish, sorted, stats } = recorder(a)

  function partition(lo, hi) {
    const pivot = a[hi]
    push(11, `Choose the last item, ${pivot}, as the pivot.`, { range: [lo, hi], pivot: [hi], vars: { lo, hi, pivot } })
    let i = lo
    for (let j = lo; j < hi; j++) {
      stats.comparisons++
      push(14, `Is ${a[j]} < pivot ${pivot}?`, { range: [lo, hi], pivot: [hi], comparing: [j], vars: { i, j, pivot } })
      if (a[j] < pivot) {
        if (i !== j) {
          ;[a[i], a[j]] = [a[j], a[i]]
          stats.swaps++
        }
        push(15, `Yes, move ${a[i]} into the "smaller" side at index ${i}.`, {
          range: [lo, hi], pivot: [hi], swapping: [i, j], vars: { i, j, pivot },
        })
        i++
      }
    }
    if (i !== hi) {
      ;[a[i], a[hi]] = [a[hi], a[i]]
      stats.swaps++
    }
    sorted.add(i)
    push(17, `Place pivot ${pivot} at index ${i}. It's now in its final position.`, {
      range: [lo, hi], swapping: [i, hi], vars: { i, pivot },
    })
    return i
  }

  function sort(lo, hi) {
    if (lo > hi) return
    if (lo === hi) {
      sorted.add(lo)
      push(4, `A single item (${a[lo]}) is already sorted.`, { range: [lo, hi], vars: { lo, hi } })
      return
    }
    push(4, `Sort indices ${lo}–${hi}.`, { range: [lo, hi], vars: { lo, hi } })
    const p = partition(lo, hi)
    sort(lo, p - 1)
    sort(p + 1, hi)
  }

  push(3, `Start with ${a.length} items.`, { vars: { lo: 0, hi: a.length - 1 } })
  sort(0, a.length - 1)
  return finish(8)
}

export const sortingAlgorithms = {
  bubble: { name: 'Bubble', code: BUBBLE, steps: bubbleSteps },
  selection: { name: 'Selection', code: SELECTION, steps: selectionSteps },
  insertion: { name: 'Insertion', code: INSERTION, steps: insertionSteps },
  merge: { name: 'Merge', code: MERGE, steps: mergeSteps },
  quick: { name: 'Quick', code: QUICK, steps: quickSteps },
}
