import { useEffect, useState } from 'react'

// A variable value shown as-is rather than as a Python literal, e.g. ListNode(3).
export class Raw {
  constructor(text) {
    this.text = text
  }
}

export const raw = (text) => new Raw(text)

/* ---------- Step player ---------- */

export function useStepPlayer(frames, { autoPlay = false } = {}) {
  const [source, setSource] = useState(frames)
  const [index, setIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [speed, setSpeed] = useState(700)

  // New frames (new input or operation) restart playback from the beginning.
  if (source !== frames) {
    setSource(frames)
    setIndex(0)
    setIsPlaying(autoPlay)
  }

  const last = frames.length - 1
  const current = Math.min(index, last)
  const finished = current >= last
  const playing = isPlaying && !finished

  useEffect(() => {
    if (!playing) return
    const timer = setTimeout(() => setIndex((i) => i + 1), speed)
    return () => clearTimeout(timer)
  }, [playing, index, speed])

  return {
    frame: frames[current],
    index: current,
    total: frames.length,
    playing,
    finished,
    speed,
    setSpeed,
    toggle() {
      if (finished) {
        setIndex(0)
        setIsPlaying(true)
      } else {
        setIsPlaying(!playing)
      }
    },
    step(delta) {
      setIsPlaying(false)
      setIndex(Math.min(last, Math.max(0, current + delta)))
    },
    reset() {
      setIsPlaying(false)
      setIndex(0)
    },
  }
}

const PRIORITY = ['swapping', 'comparing', 'found', 'pivot', 'sorted']

export function stateOf(index, frame) {
  for (const state of PRIORITY) {
    if (frame[state]?.includes(index)) return state
  }
  if (frame.range && (index < frame.range[0] || index > frame.range[1])) return 'dim'
  return ''
}

// Lay out a binary tree using in-order position for x and depth for y.
export function layoutBinaryTree(root, getChildren, gapX = 56, gapY = 70) {
  const positions = {}
  let order = 0
  function visit(id, depth) {
    if (id === null || id === undefined) return
    const [left, right] = getChildren(id)
    visit(left, depth + 1)
    positions[id] = { x: order++ * gapX, y: depth * gapY }
    visit(right, depth + 1)
  }
  visit(root, 0)
  return positions
}

export function parseNumbers(text, { maxLength = 12, min = -99, max = 99 } = {}) {
  const parts = text.split(',').map((part) => part.trim()).filter(Boolean)
  if (parts.length === 0) return { error: 'Enter at least one number.' }
  if (parts.length > maxLength) return { error: `Use at most ${maxLength} numbers.` }
  const values = parts.map(Number)
  if (values.some((v) => !Number.isInteger(v) || v < min || v > max)) {
    return { error: `Use whole numbers between ${min} and ${max}.` }
  }
  return { values }
}

export function randomInts(count, min = 1, max = 99) {
  return Array.from({ length: count }, () => Math.floor(Math.random() * (max - min + 1)) + min)
}
