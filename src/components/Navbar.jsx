import { NavLink, Link } from 'react-router-dom'
import { useAuth } from '../auth'

const links = [
  { to: '/', label: 'Learn', end: true },
  { to: '/problems', label: 'Problems' },
  { to: '/playground', label: 'Playground' },
  { to: '/dashboard', label: 'Progress' },
]

function Navbar() {
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
