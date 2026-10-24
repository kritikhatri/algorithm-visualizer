import BinarySearch from './BinarySearch'
import BinarySearchTree from './BinarySearchTree'
import DPTable from './DPTable'
import GraphTraversal from './GraphTraversal'
import Growth from './Growth'
import HashTable from './HashTable'
import Heap from './Heap'
import LinkedList from './LinkedList'
import RecursionTree from './RecursionTree'
import Sorting from './Sorting'
import StackQueue from './StackQueue'
import TwoPointers from './TwoPointers'

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
}
