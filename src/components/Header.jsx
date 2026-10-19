
function Header({ apiStatus }) {
  const isOnline = apiStatus === 'Algorithm Visualizer API is running!'

  return (
    <header className="page-header">
      <p className="eyebrow">
        LEARN • VISUALIZE • UNDERSTAND
      </p>

      <h1>Algorithm Visualizer</h1>

      <p className="subtitle">
        Watch sorting algorithms come to life, one step at a time.
      </p>

      <p className="api-status" aria-live="polite">
        <span
          className={`status-dot ${
            isOnline ? 'status-online' : 'status-offline'
          }`}
        />

        Backend: {apiStatus}
      </p>
    </header>
  )
}

export default Header
