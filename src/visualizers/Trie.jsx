import { useState } from 'react'
import { GraphView, PlayerControls, VizLayout } from './common'
import { layoutTree, useStepPlayer } from './helpers'

const CODE = `class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word):
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return "$" in node

    def starts_with(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True`

// The trie is stored as a map from prefix ('' is the root) to { children, end }.
const ROOT = ''

function insertSteps(trie, word) {
  const frames = []
  let next = trie
  const path = [ROOT]
  frames.push({ trie: next, line: 6, message: `Insert "${word}": start at the root.`, current: ROOT, path: [...path], vars: { word } })

  for (let i = 0; i < word.length; i++) {
    const parent = word.slice(0, i)
    const prefix = word.slice(0, i + 1)
    const exists = Boolean(next[prefix])
    if (!exists) {
      next = {
        ...next,
        [parent]: { ...next[parent], children: [...next[parent].children, prefix].sort() },
        [prefix]: { children: [], end: false },
      }
    }
    path.push(prefix)
    frames.push({
      trie: next,
      line: 8,
      message: exists ? `'${word[i]}' already exists. Follow it.` : `No '${word[i]}' child yet. Create it.`,
      current: prefix,
      created: exists ? [] : [prefix],
      path: [...path],
      vars: { word, ch: word[i] },
    })
  }

  next = { ...next, [word]: { ...next[word], end: true } }
  frames.push({ trie: next, line: 9, message: `Mark the last node as the end of "${word}".`, current: word, path, found: [word], vars: { word } })
  return frames
}

function walkSteps(trie, text, isSearch) {
  const frames = []
  const offset = isSearch ? 0 : 8
  const path = [ROOT]
  frames.push({ trie, line: 12 + offset, message: `${isSearch ? 'Search for' : 'Prefix'} "${text}": start at the root.`, current: ROOT, path: [...path], vars: { text } })

  for (let i = 0; i < text.length; i++) {
    const prefix = text.slice(0, i + 1)
    if (!trie[prefix]) {
      frames.push({ trie, line: 15 + offset, message: `No '${text[i]}' child here, so return False.`, current: text.slice(0, i), path, missing: true, vars: { text, ch: text[i], result: false } })
      return frames
    }
    path.push(prefix)
    frames.push({ trie, line: 16 + offset, message: `Found '${text[i]}'. Move down.`, current: prefix, path: [...path], vars: { text, ch: text[i] } })
  }

  if (isSearch) {
    const ok = trie[text].end
    frames.push({
      trie,
      line: 17,
      message: ok ? `"${text}" ends here: it's a stored word → True.` : `The path exists, but no word ends here → False.`,
      current: text,
      path,
      found: ok ? [text] : [],
      vars: { text, result: ok },
    })
  } else {
    frames.push({ trie, line: 25, message: `Every letter of "${text}" was found → True.`, current: text, path, found: [text], vars: { text, result: true } })
  }
  return frames
}

function build(words) {
  let trie = { [ROOT]: { children: [], end: false } }
  for (const word of words) trie = insertSteps(trie, word).at(-1).trie
  return trie
}

const START = [{ trie: build(['car', 'cart', 'care', 'cat', 'dog']), message: 'Insert a word, search for one, or check a prefix.' }]

function Trie() {
  const [frames, setFrames] = useState(START)
  const [word, setWord] = useState('cap')
  const [error, setError] = useState('')
  const player = useStepPlayer(frames, { autoPlay: true })
  const { frame } = player
  const trie = frames.at(-1).trie

  function run(op) {
    const text = word.trim().toLowerCase()
    if (!/^[a-z]{1,8}$/.test(text)) {
      setError('Use 1–8 letters.')
      return
    }
    if (op === 'insert' && Object.keys(trie).length + text.length > 32) {
      setError('The trie is full for this demo. Reset it first.')
      return
    }
    setError('')
    setFrames(op === 'insert' ? insertSteps(trie, text) : walkSteps(trie, text, op === 'search'))
  }

  const shown = frame.trie
  const positions = layoutTree([ROOT], (id) => shown[id].children, 48, 62)
  const nodes = Object.entries(shown).map(([id, node]) => ({
    id,
    label: id === ROOT ? '•' : id.at(-1),
    ...positions[id],
    note: node.end ? '✓' : undefined,
    state: frame.found?.includes(id)
      ? 'found'
      : frame.current === id
        ? frame.missing ? 'swapping' : 'comparing'
        : frame.created?.includes(id)
          ? 'found'
          : frame.path?.includes(id)
            ? 'pivot'
            : node.end ? 'sorted' : '',
  }))
  const edges = Object.entries(shown).flatMap(([id, node]) =>
    node.children.map((child) => ({ from: id, to: child, state: frame.path?.includes(child) ? 'active' : '' }))
  )

  return (
    <VizLayout
      toolbar={
        <form className="inline-form" onSubmit={(event) => { event.preventDefault(); run('insert') }}>
          <label>
            <span>Word</span>
            <input value={word} maxLength={8} onChange={(event) => setWord(event.target.value)} />
          </label>
          <button className="button primary small" type="submit">insert</button>
          <button className="button ghost small" type="button" onClick={() => run('search')}>search</button>
          <button className="button ghost small" type="button" onClick={() => run('prefix')}>starts_with</button>
          <button className="button ghost small" type="button" onClick={() => setFrames(START)}>Reset</button>
          {error && <span className="error-text">{error}</span>}
        </form>
      }
      visual={<GraphView nodes={nodes} edges={edges} height={360} />}
      legend={[['comparing', 'Current node'], ['pivot', 'Path'], ['found', 'New / matched'], ['sorted', 'Word ends here (✓)']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default Trie
