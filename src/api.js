const TOKEN_KEY = 'algorithm-visualizer-token'

export function getToken() {
  try {
    return localStorage.getItem(TOKEN_KEY)
  } catch {
    return null
  }
}

export function setToken(token) {
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token)
    else localStorage.removeItem(TOKEN_KEY)
  } catch {
    // Storage can be unavailable (private mode); the session just won't persist.
  }
}

export async function api(path, { method = 'GET', body } = {}) {
  const token = getToken()
  const response = await fetch(`/api${path}`, {
    method,
    headers: {
      ...(body && { 'Content-Type': 'application/json' }),
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: body && JSON.stringify(body),
  })

  if (response.status === 204) return null

  const data = await response.json().catch(() => ({}))

  if (!response.ok) {
    const error = new Error(data.error || 'Request failed.')
    error.status = response.status
    throw error
  }

  return data
}
