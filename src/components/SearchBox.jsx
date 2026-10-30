import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api'

const GROUPS = [
  ['topics', 'Topics', (r) => `/topics/${r.id}`],
  ['problems', 'Problems', (r) => `/problems/${r.id}`],
  ['flashcards', 'Flashcards', (r) => `/topics/${r.topic}/cards`],
]

function SearchBox() {
  const navigate = useNavigate()
  const box = useRef(null)
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(null)

  useEffect(() => {
    const q = query.trim()
    if (q.length < 2) return
    let cancelled = false
    const timer = setTimeout(() => {
      api(`/search?${new URLSearchParams({ q })}`)
        .then((data) => !cancelled && setResults(data))
        .catch(() => !cancelled && setResults(null))
    }, 150)
    return () => {
      cancelled = true
      clearTimeout(timer)
    }
  }, [query])

  useEffect(() => {
    function close(event) {
      if (!box.current?.contains(event.target)) setQuery('')
    }
    document.addEventListener('mousedown', close)
    return () => document.removeEventListener('mousedown', close)
  }, [])

  function go(path) {
    setQuery('')
    navigate(path)
  }

  const open = query.trim().length >= 2 && results
  const empty = open && GROUPS.every(([key]) => results[key].length === 0)

  return (
    <div className="search" ref={box}>
      <input
        type="search"
        aria-label="Search topics, problems and flashcards"
        placeholder="Search…"
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        onKeyDown={(event) => event.key === 'Escape' && setQuery('')}
      />
      {open && (
        <div className="search-results">
          {empty && <p className="muted">No matches.</p>}
          {GROUPS.map(([key, label, pathOf]) => results[key].length > 0 && (
            <div key={key}>
              <h3>{label}</h3>
              {results[key].map((result) => (
                <button key={result.id} onClick={() => go(pathOf(result))}>{result.title}</button>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default SearchBox
