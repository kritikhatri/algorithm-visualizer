
function ArrayVisualizer({
  array,
  comparing = [],
  swapping = [],
  sorted = [],
}) {
  const maxValue = Math.max(...array.map((number) => Math.abs(number)), 1)

  return (
    <section className="visualizer-bars">
      {array.map((number, index) => {
        let barClass = 'bar'

        if (swapping.includes(index)) {
          barClass += ' bar-swapping'
        } else if (comparing.includes(index)) {
          barClass += ' bar-comparing'
        } else if (sorted.includes(index)) {
          barClass += ' bar-sorted'
        }

        return (
          <div className="bar-container" key={index}>
            <div
              className={barClass}
              style={{
                height: `${Math.max((Math.abs(number) / maxValue) * 180, 12)}px`,
              }}
            >
              <span>{number}</span>
            </div>
          </div>
        )
      })}
    </section>
  )
}

export default ArrayVisualizer
