function ArrayVisualizer({ array }) {
  return (
    <div className="array-visualizer">
    <p className="array-label">Array Visualization</p>
      {(array.length ? array : [0]).map((number, index) => (
        <div
          key={index}
          className="array-bar"
          style={{ height: `${(number / Math.max(...array)) * 180}px` }}
        >
            {number}
        </div>
      ))}
    </div>
  )
}

export default ArrayVisualizer