import BinarySearch from './BinarySearch'
import Bits from './Bits'
import BinarySearchTree from './BinarySearchTree'
import DPTable from './DPTable'
import Dijkstra from './Dijkstra'
import GraphTraversal from './GraphTraversal'
import Growth from './Growth'
import HashTable from './HashTable'
import Intervals from './Intervals'
import Heap from './Heap'
import LinkedList from './LinkedList'
import RecursionTree from './RecursionTree'
import SlidingWindow from './SlidingWindow'
import Sorting from './Sorting'
import StackQueue from './StackQueue'
import Trie from './Trie'
import TwoPointers from './TwoPointers'
import UnionFind from './UnionFind'

// Keys match each topic's `visualizer` field from the API.
export const visualizers = {
  growth: Growth,
  'two-pointers': TwoPointers,
  'hash-table': HashTable,
  'linked-list': LinkedList,
  'stack-queue': StackQueue,
  'recursion-tree': RecursionTree,
  sorting: Sorting,
  'binary-search': BinarySearch,
  bst: BinarySearchTree,
  heap: Heap,
  graph: GraphTraversal,
  'dp-table': DPTable,
  bits: Bits,
  'sliding-window': SlidingWindow,
  trie: Trie,
  dijkstra: Dijkstra,
  'union-find': UnionFind,
  intervals: Intervals,
}
