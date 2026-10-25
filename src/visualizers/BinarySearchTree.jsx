import { useState } from 'react'
import { GraphView, PlayerControls, VizLayout } from './common'
import { layoutBinaryTree, randomInts, useStepPlayer } from './helpers'

const CODE = `def insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root

def search(root, val):
    while root:
        if val == root.val:
            return True
        root = root.left if val < root.val else root.right
    return False

def inorder(root, out):
    if root:
        inorder(root.left, out)
        out.append(root.val)
        inorder(root.right, out)`

const EMPTY = { root: null, nodes: {}, nextId: 0 }

function insertSteps(tree, val) {
  const frames = []
  const push = (t, line, message, extra = {}) => frames.push({ tree: t, line, message, vars: { val }, ...extra })

  function attach(t, parentId, side) {
    const id = t.nextId
    const nodes = { ...t.nodes, [id]: { val, left: null, right: null } }
    if (parentId !== null) nodes[parentId] = { ...nodes[parentId], [side]: id }
    return { tree: { root: t.root ?? id, nodes, nextId: id + 1 }, id }
  }

  if (tree.root === null) {
    const { tree: next, id } = attach(tree, null)
    push(next, 3, `The tree is empty, so ${val} becomes the root.`, { found: [id] })
    return frames
  }

  const path = []
  let id = tree.root
  for (;;) {
    const node = tree.nodes[id]
    path.push(id)
    if (val === node.val) {
      push(tree, 8, `${val} is already in the tree. This BST keeps values unique.`, { found: [id], path: [...path] })
      return frames
    }
    const side = val < node.val ? 'left' : 'right'
    push(tree, val < node.val ? 5 : 7, `${val} ${val < node.val ? '<' : '>'} ${node.val}, so go ${side}.`, {
      current: id,
      path: [...path],
    })
    if (node[side] === null) {
      const { tree: next, id: newId } = attach(tree, id, side)
      push(next, 3, `Found an empty spot: create TreeNode(${val}) as the ${side} child of ${node.val}.`, {
        found: [newId],
        path: [...path],
      })
      return frames
    }
    id = node[side]
  }
}

function searchSteps(tree, val) {
  const frames = []
  const push = (line, message, extra = {}) => frames.push({ tree, line, message, vars: { val }, ...extra })
  const path = []
  let id = tree.root

  while (id !== null) {
    const node = tree.nodes[id]
    path.push(id)
    push(12, `Compare ${val} with ${node.val}.`, { current: id, path: [...path] })
    if (val === node.val) {
      push(13, `Found ${val} after ${path.length} comparison(s).`, { found: [id], path: [...path] })
      return frames
    }
    push(14, `${val} ${val < node.val ? '<' : '>'} ${node.val}, so go ${val < node.val ? 'left' : 'right'}.`, {
      current: id,
      path: [...path],
    })
    id = val < node.val ? node.left : node.right
  }
  push(15, `Fell off the tree: ${val} is not in the BST.`, { path })
  return frames
}

function inorderSteps(tree) {
  const frames = []
  const out = []
  const visited = []
  function visit(id) {
    if (id === null) return
    const node = tree.nodes[id]
    visit(node.left)
    out.push(node.val)
    visited.push(id)
    frames.push({
      tree,
      line: 20,
      message: `Visit ${node.val}. Output so far: [${out.join(', ')}]`,
      current: id,
      visited: [...visited],
      vars: { out: [...out] },
    })
    visit(node.right)
  }
  visit(tree.root)
  frames.push({
    tree,
    line: 21,
    message: `In-order traversal of a BST gives sorted values: [${out.join(', ')}]`,
    visited,
    vars: { out },
  })
  return frames
}

function buildTree(values) {
  return values.reduce((tree, value) => insertSteps(tree, value).at(-1).tree, EMPTY)
}

const START_TREE = buildTree([50, 30, 70, 20, 40, 60, 80, 35])
const START = [{ tree: START_TREE, message: 'Insert or search for a value, or run an in-order traversal.' }]

function BinarySearchTree() {
  const [frames, setFrames] = useState(START)
  const [value, setValue] = useState(45)
  const player = useStepPlayer(frames, { autoPlay: true })
  const { frame } = player
  const tree = frames.at(-1).tree

  function run(op) {
    if (op !== 'inorder' && !Number.isInteger(value)) return
    if (op === 'insert' && Object.keys(tree.nodes).length >= 15) {
      setFrames([{ tree, message: 'The tree is full for this demo (15 nodes). Clear it to start again.' }])
      return
    }
    const steps = op === 'insert' ? insertSteps(tree, value) : op === 'search' ? searchSteps(tree, value) : inorderSteps(tree)
    setFrames(steps.length ? steps : [{ tree, message: 'The tree is empty.' }])
  }

  const shown = frame.tree
  const positions = layoutBinaryTree(shown.root, (id) => [shown.nodes[id].left, shown.nodes[id].right])
  const nodes = Object.entries(shown.nodes).map(([key, node]) => {
    const id = Number(key)
    return {
      id,
      label: node.val,
      ...positions[id],
      state: frame.found?.includes(id)
        ? 'found'
        : frame.current === id
          ? 'comparing'
          : frame.visited?.includes(id)
            ? 'sorted'
            : frame.path?.includes(id)
              ? 'pivot'
              : '',
    }
  })
  const edges = Object.entries(shown.nodes).flatMap(([key, node]) =>
    [node.left, node.right]
      .filter((child) => child !== null)
      .map((child) => ({ from: Number(key), to: child, state: frame.path?.includes(child) ? 'active' : '' }))
  )

  return (
    <VizLayout
      toolbar={
        <form className="inline-form" onSubmit={(event) => { event.preventDefault(); run('insert') }}>
          <label>
            <span>Value</span>
            <input type="number" value={value} min={-99} max={999} onChange={(event) => setValue(Number(event.target.value))} />
          </label>
          <button className="button primary small" type="submit">Insert</button>
          <button className="button ghost small" type="button" onClick={() => run('search')}>Search</button>
          <button className="button ghost small" type="button" onClick={() => run('inorder')}>In-order</button>
          <button className="button ghost small" type="button" onClick={() => setFrames([{ tree: buildTree(randomInts(8, 1, 99)), message: 'A random BST.' }])}>⚄ Random</button>
          <button className="button ghost small" type="button" onClick={() => setFrames([{ tree: EMPTY, message: 'Empty tree. Insert a value to start.' }])}>Clear</button>
        </form>
      }
      visual={<GraphView nodes={nodes} edges={edges} height={360} />}
      legend={[['comparing', 'Current node'], ['pivot', 'Path taken'], ['found', 'Found / inserted'], ['sorted', 'Visited']]}
      message={frame.message}
      controls={<PlayerControls player={player} />}
      code={CODE}
      line={frame.line}
      vars={frame.vars}
    />
  )
}

export default BinarySearchTree
