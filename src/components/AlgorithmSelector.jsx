
function AlgorithmSelector({ algorithm, setAlgorithm }) {
  return (
    <section className="algorithm-selector">
      <label htmlFor="algorithm">Choose an algorithm</label>

      <select
        id="algorithm"
        value={algorithm}
        onChange={(event) => setAlgorithm(event.target.value)}
      >
        <option value="bubble">Bubble Sort</option>
        <option value="selection">Selection Sort</option>
        <option value="insertion">Insertion Sort</option>
        <option value="merge">Merge Sort</option>
        <option value="quick">Quick Sort</option>
      </select>
    </section>
  )
}

export default AlgorithmSelector
