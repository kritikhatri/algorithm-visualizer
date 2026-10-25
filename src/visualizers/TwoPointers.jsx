import { useMemo, useState } from 'react'
import { ArrayCells, NumberListInput, PlayerControls, VizLayout } from './common'
import { useStepPlayer } from './helpers'

const CODE = `def pair_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return []`

function pairSumSteps(nums, target) {
  const frames = []
  const push = (line, message, left, right, extra = {}) =>
    frames.push({
      array: nums,
      line,
      message,
      pointers: { left, right },
      range: [left, right],
      vars: { target, left, right, ...extra.vars },
      ...extra,
    })

  let left = 0
  let right = nums.length - 1
  push(2, 'Put one pointer at each end of the sorted list.', left, right)

  while (left < right) {
    const total = nums[left] + nums[right]
    push(4, `${nums[left]} + ${nums[right]} = ${total}`, left, right, {
      comparing: [left, right],
      vars: { total },
    })
    if (total === target) {
      push(6, `Found it! Indices [${left}, ${right}] add up to ${target}.`, left, right, {
        found: [left, right],
        vars: { total },
      })
      return frames
    }
    if (total < target) {
      push(8, `${total} < ${target}: the sum is too small, so move left → right.`, left + 1, right, { vars: { total } })
      left++
    } else {
      push(10, `${total} > ${target}: the sum is too big, so move right → left.`, left, right - 1, { vars: { total } })
      right--
    }
  }
  push(11, `The pointers met. No pair adds up to ${target}.`, left, right)
  return frames
}

function TwoPointers() {
  const [nums, setNums] = useState([1, 3, 4, 6, 8, 11, 14])
  const [target, setTarget] = useState(17)

  const frames = useMemo(() => pairSumSteps(nums, target), [nums, target])
  const player = useStepPlayer(frames)
  const { frame } = player

  return (
    <VizLayout
      toolbar={
        <>
          <NumberListInput
            initial={nums}
            label="Sorted list"
            onSubmit={(values) => setNums([...values].sort((a, b) => a - b))}
            maxLength={12}
          />
          <label className="inline-field">
            <span>Target</span>
            <input
              type="number"
              value={target}
              onChange={(event) => setTarget(Number(event.target.value))}
            />
          </label>
        </>
      }
      visual={<ArrayCells frame={frame} />}
      legend={[
        ['comparing', 'Current pair'],
        ['found', 'Answer'],
        ['dim', 'Ruled out'],
      ]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default TwoPointers
