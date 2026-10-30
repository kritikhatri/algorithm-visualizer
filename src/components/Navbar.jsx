import { useState } from 'react'
import { NavLink, Link } from 'react-router-dom'
import { useAuth } from '../auth'
import SearchBox from './SearchBox'

const links = [
  { to: '/', label: 'Learn', end: true },
  { to: '/problems', label: 'Problems' },
  { to: '/flashcards', label: 'Flashcards' },
  { to: '/playground', label: 'Playground' },
  { to: '/race', label: 'Race' },
  { to: '/cheatsheet', label: 'Cheat sheet' },
  { to: '/dashboard', label: 'Progress' },
]

function readTheme() {
  try {
    return localStorage.getItem('dsa-theme') === 'light' ? 'light' : 'dark'
  } catch {
    return 'dark'
  }
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme
  document.documentElement.style.colorScheme = theme
}

applyTheme(readTheme())

function Navbar() {
  const [theme, setTheme] = useState(readTheme)

  function toggleTheme() {
    const next = theme === 'dark' ? 'light' : 'dark'
    setTheme(next)
    applyTheme(next)
    try {
      localStorage.setItem('dsa-theme', next)
    } catch {
      // The choice just won't persist.
    }
  }

  const { user, openAuth, signOut } = useAuth()

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="brand">
          <span className="brand-mark" aria-hidden="true">
            <i /><i /><i /><i />
          </span>
          <span>DSA Study Lab</span>
        </Link>

        <nav className="nav-links" aria-label="Main">
          {links.map((link) => (
            <NavLink key={link.to} to={link.to} end={link.end} className="nav-link">
              {link.label}
            </NavLink>
          ))}
        </nav>

        <SearchBox />
        <button
          className="button ghost small icon-toggle"
          onClick={toggleTheme}
          aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
        >
          {theme === 'dark' ? '☀' : '☾'}
        </button>

        <div className="nav-auth">
          {user ? (
            <>
              <span className="user-chip">{user.username}</span>
              <button className="button ghost small" onClick={signOut}>Log out</button>
            </>
          ) : (
            <button className="button primary small" onClick={openAuth}>Log in</button>
          )}
        </div>
      </div>
    </header>
  )
}

export default Navbar
