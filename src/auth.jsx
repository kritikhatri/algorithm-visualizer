import { createContext, useCallback, useContext, useEffect, useState } from 'react'
import { api, getToken, setToken } from './api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [progress, setProgress] = useState(null)
  const [authOpen, setAuthOpen] = useState(false)

  const refreshProgress = useCallback(() => {
    return api('/progress')
      .then(setProgress)
      .catch(() => setProgress(null))
  }, [])

  useEffect(() => {
    if (!getToken()) return
    api('/auth/me')
      .then((data) => {
        setUser(data.user)
        refreshProgress()
      })
      .catch(() => setToken(null))
  }, [refreshProgress])

  function signIn({ token, user }) {
    setToken(token)
    setUser(user)
    setAuthOpen(false)
    refreshProgress()
  }

  function signOut() {
    setToken(null)
    setUser(null)
    setProgress(null)
  }

  const value = {
    user,
    progress,
    refreshProgress,
    signIn,
    signOut,
    authOpen,
    openAuth: () => setAuthOpen(true),
    closeAuth: () => setAuthOpen(false),
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// eslint-disable-next-line react/only-export-components
export function useAuth() {
  return useContext(AuthContext)
}
