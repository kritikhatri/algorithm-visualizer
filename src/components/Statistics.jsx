
function Statistics({ array }) {
  if (array.length === 0) {
    return (
      <section className="panel">
        <p>Array Size: 0</p>
        <p>Minimum: —</p>
        <p>Maximum: —</p>
      </section>
    )
  }

  return (
    <section className="panel">
        <h3>Array Statistics</h3>
        <p>Array Size: {array.length}</p>
        <p>Minimum: {Math.min(...array)}</p>
        <p>Maximum: {Math.max(...array)}</p>
    </section>
  )
}

export default Statistics
