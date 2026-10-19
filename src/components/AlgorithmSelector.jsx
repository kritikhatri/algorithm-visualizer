function AlgorithmSelector({ algorithm, setAlgorithm }) {
  return (
    <section className="panel">
      <label htmlFor="algorithm">Choose Algorithm</label>

      <select
        id="algorithm"
        value={algorithm}
        onChange={(event) => setAlgorithm(event.target.value)}
      >
        <option value="bubble">Bubble Sort</option>
        <option value="selection">Selection Sort</option>
        <option value="insertion">Insertion Sort</option>
      </select>
    </section>
  )
}

export default AlgorithmSelector