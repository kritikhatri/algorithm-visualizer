import { useEffect, useState } from 'react'

const START = [42, 17, 88, 23, 65, 9, 54, 31]

const CODE = [
  'for i in range(n):',
  '    for j in range(n - i - 1):',
  '        if nums[j] > nums[j + 1]:',
  '            swap(nums, j, j + 1)',
]

function buildFrames() {
  const nums = [...START]
  const frames = []
  for (let i = 0; i < nums.length; i++) {
    for (let j = 0; j < nums.length - i - 1; j++) {
      frames.push({ nums: [...nums], active: [j, j + 1], line: 2, done: i })
      if (nums[j] > nums[j + 1]) {
        ;[nums[j], nums[j + 1]] = [nums[j + 1], nums[j]]
        frames.push({ nums: [...nums], active: [j, j + 1], line: 3, swapped: true, done: i })
      }
    }
  }
  frames.push({ nums: [...nums], active: [], line: 0, done: nums.length })
  return frames
}

const FRAMES = buildFrames()

// A looping bubble sort that previews what the real visualizers do.
function HeroDemo() {
  const [index, setIndex] = useState(0)
  const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
  const frame = reduceMotion ? FRAMES.at(-1) : FRAMES[index]

  useEffect(() => {
    if (reduceMotion) return
    const delay = index === FRAMES.length - 1 ? 2200 : 420
    const timer = setTimeout(() => setIndex((i) => (i + 1) % FRAMES.length), delay)
    return () => clearTimeout(timer)
  }, [index, reduceMotion])

  return (
    <div className="hero-demo" aria-hidden="true">
      <div className="demo-bar">
        <i /><i /><i />
        <span>bubble_sort.py</span>
      </div>
      <div className="demo-bars">
        {frame.nums.map((value, i) => {
          const settled = i >= frame.nums.length - frame.done
          const state = frame.active.includes(i)
            ? frame.swapped ? 'swapping' : 'comparing'
            : settled ? 'sorted' : ''
          return (
            <div className="demo-slot" key={i}>
              <div className={`bar ${state}`} style={{ height: `${value}%` }} />
              <span>{value}</span>
            </div>
          )
        })}
      </div>
      <pre className="demo-code">
        {CODE.map((text, i) => (
          <span className={frame.line === i && frame.active.length ? 'on' : ''} key={text}>{text}{'\n'}</span>
        ))}
      </pre>
    </div>
  )
}

export default HeroDemo
