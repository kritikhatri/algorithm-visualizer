
function ArrayControls({
  input,
  setInput,
  onSubmit,
  onGenerate,
  onReset,
}) {
  return (
    <section className="panel">
      <form className="input-section" onSubmit={onSubmit}>
        <label htmlFor="array-input">Your array</label>

        <div className="input-row">
          <input
            id="array-input"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            placeholder="e.g. 8, 3, 6, 1, 5"
          />

          <button className="primary-button" type="submit">
            Visualize
          </button>
        </div>

        <p className="helper-text">
          Enter up to 12 whole numbers separated by commas.
        </p>
      </form>

      <div className="array-controls">
        <button
          className="secondary-button"
          type="button"
          onClick={onGenerate}
        >
          Generate Random Array
        </button>

        <button
          className="secondary-button"
          type="button"
          onClick={onReset}
        >
          Reset Array
        </button>
      </div>
    </section>
  )
}

export default ArrayControls
