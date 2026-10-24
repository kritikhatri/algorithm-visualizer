import { useEffect, useState } from 'react'
import { api } from '../api'
import { useAuth } from '../auth'

function AuthModal() {
  const { signIn, closeAuth } = useAuth()
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ email: '', username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const isLogin = mode === 'login'

  useEffect(() => {
    function handleKey(event) {
      if (event.key === 'Escape') closeAuth()
    }
    window.addEventListener('keydown', handleKey)
    return () => window.removeEventListener('keydown', handleKey)
  }, [closeAuth])

  function update(field) {
    return (event) => setForm({ ...form, [field]: event.target.value })
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      signIn(await api(isLogin ? '/auth/login' : '/auth/register', { method: 'POST', body: form }))
    } catch (err) {
      setError(err.message)
      setLoading(false)
    }
  }

  return (
    <div className="modal-backdrop" onMouseDown={closeAuth}>
      <div
        className="modal card"
        role="dialog"
        aria-modal="true"
        aria-labelledby="auth-title"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <button className="modal-close" onClick={closeAuth} aria-label="Close">✕</button>

        <h2 id="auth-title" className="card-title large">
          {isLogin ? 'Welcome back' : 'Create an account'}
        </h2>
        <p className="muted">
          {isLogin
            ? 'Log in to pick up where you left off.'
            : 'Track topics, solved problems and quiz scores.'}
        </p>

        <form className="auth-form" onSubmit={handleSubmit}>
          <label>
            Email
            <input type="email" required autoFocus value={form.email} onChange={update('email')} />
          </label>

          {!isLogin && (
            <label>
              Username
              <input required minLength={3} maxLength={20} value={form.username} onChange={update('username')} />
            </label>
          )}

          <label>
            Password
            <input
              type="password"
              required
              minLength={isLogin ? undefined : 8}
              autoComplete={isLogin ? 'current-password' : 'new-password'}
              value={form.password}
              onChange={update('password')}
            />
          </label>

          {error && <p className="error-text">{error}</p>}

          <button className="button primary full" type="submit" disabled={loading}>
            {loading ? 'Please wait…' : isLogin ? 'Log in' : 'Sign up'}
          </button>
        </form>

        <p className="switch-mode">
          {isLogin ? 'New here?' : 'Already have an account?'}{' '}
          <button
            className="link"
            onClick={() => {
              setMode(isLogin ? 'register' : 'login')
              setError('')
            }}
          >
            {isLogin ? 'Create an account' : 'Log in'}
          </button>
        </p>
      </div>
    </div>
  )
}

export default AuthModal
