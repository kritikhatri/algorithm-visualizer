import { useMemo } from 'react'
import { marked } from 'marked'

// Content comes from our own API, so rendering it as HTML is safe.
function Markdown({ source, className = '' }) {
  const html = useMemo(() => marked.parse(source ?? ''), [source])
  return <div className={`prose ${className}`} dangerouslySetInnerHTML={{ __html: html }} />
}

export default Markdown
