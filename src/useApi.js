import { useEffect, useState } from 'react'
import { api } from './api'

export function useApi(path) {
  const [state, setState] = useState({ path: null, data: null, error: null })

  useEffect(() => {
    if (!path) return
    let cancelled = false
    api(path)
      .then((data) => !cancelled && setState({ path, data, error: null }))
      .catch((error) => !cancelled && setState({ path, data: null, error }))
    return () => {
      cancelled = true
    }
  }, [path])

  // Ignore results that belong to a previous path while the new one loads.
  const current = state.path === path || !path
  return {
    data: current ? state.data : null,
    error: current ? state.error : null,
    loading: !current,
  }
}
