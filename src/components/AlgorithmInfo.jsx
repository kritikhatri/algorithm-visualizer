function AlgorithmInfo({ algorithm }) {
  const info = {
    bubble: 'O(n²)',
    selection: 'O(n²)',
    insertion: 'O(n²)',
  }

  return (
  <div className="complexity-info">
    <p>Time Complexity: {info[algorithm]}</p>
    <p>Space Complexity: O(n)</p>
    <p>Algorithm: {algorithm.charAt(0).toUpperCase() + algorithm.slice(1)} Sort</p>
  </div>
)
}

export default AlgorithmInfo