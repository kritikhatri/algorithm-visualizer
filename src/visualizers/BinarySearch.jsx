import { useMemo, useState } from 'react'
import { ArrayCells, PlayerControls, VizLayout } from './common'
import { useStepPlayer } from './helpers'

const CODE = `def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1`

const NUMS = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 81, 91]

function searchSteps(nums, target) {
  const frames = []
  const push = (line, message, lo, hi, extra = {}) =>
    frames.push({
      array: nums,
      line,
      message,
      range: [lo, hi],
      pointers: { lo, hi, ...(extra.mid !== undefined && { mid: extra.mid }) },
      vars: { target, lo, hi, ...(extra.mid !== undefined && { mid: extra.mid }) },
      ...extra,
    })

  let lo = 0
  let hi = nums.length - 1
  push(2, `Search the whole list for ${target}.`, lo, hi)

  while (lo <= hi) {
    const mid = Math.floor((lo + hi) / 2)
    push(4, `Check the middle: index ${mid} holds ${nums[mid]}.`, lo, hi, { mid, comparing: [mid] })
    if (nums[mid] === target) {
      push(6, `Found ${target} at index ${mid} after ${frames.filter((f) => f.line === 4).length} checks.`, lo, hi, {
        mid,
        found: [mid],
      })
      return frames
    }
    if (nums[mid] < target) {
      push(8, `${nums[mid]} < ${target}, so discard the left half.`, mid + 1, hi, { mid })
      lo = mid + 1
    } else {
      push(10, `${nums[mid]} > ${target}, so discard the right half.`, lo, mid - 1, { mid })
      hi = mid - 1
    }
  }
  push(11, `lo passed hi, so ${target} isn't in the list. It would be inserted at index ${lo}.`, lo, hi)
  return frames
}

function BinarySearch() {
  const [target, setTarget] = useState(56)
  const frames = useMemo(() => searchSteps(NUMS, target), [target])
  const player = useStepPlayer(frames)
  const { frame } = player

  return (
    <VizLayout
      toolbar={
        <>
          <label className="inline-field">
            <span>Find</span>
            <input type="number" value={target} onChange={(event) => setTarget(Number(event.target.value))} />
          </label>
          <span className="muted">Tip: click any cell to search for it, or try a missing value like 40.</span>
        </>
      }
      visual={<ArrayCells frame={frame} onCellClick={setTarget} />}
      legend={[
        ['comparing', 'mid'],
        ['found', 'Found'],
        ['dim', 'Discarded'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default BinarySearch
