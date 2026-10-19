function SortButton({ onSort , isSorting }) {
  return (
    <button
      className="primary-button"
      onClick={onSort}
    >
      {isSorting ? 'Sorting...' : 'Start Sorting'}
    </button>
  )
}

export default SortButton