// Show JSON test values the way Python would print them.
export function pyRepr(value) {
  if (value === null || value === undefined) return 'None'
  if (value === true) return 'True'
  if (value === false) return 'False'
  if (typeof value === 'string') return `'${value.replace(/'/g, "\\'")}'`
  if (Array.isArray(value)) return `[${value.map(pyRepr).join(', ')}]`
  if (typeof value === 'object') {
    return `{${Object.entries(value).map(([k, v]) => `${pyRepr(k)}: ${pyRepr(v)}`).join(', ')}}`
  }
  return String(value)
}

export function formatArgs(args) {
  return args.map(pyRepr).join(', ')
}
