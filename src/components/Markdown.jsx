import { useMemo } from 'react'
import { marked } from 'marked'
import { GLOSSARY } from '../utils/glossary'

const SKIP = 'code, pre, a, h1, h2, h3, abbr, th'

// Mark the first use of each glossary term in the text with a hover/focus tooltip.
function addGlossary(html) {
  const doc = new DOMParser().parseFromString(html, 'text/html')
  for (const [term, definition] of Object.entries(GLOSSARY)) {
    const pattern = new RegExp(`\\b${term.replace(' ', '[ -]')}\\b`, 'i')
    const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT)
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      if (node.parentElement.closest(SKIP)) continue
      const match = pattern.exec(node.data)
      if (!match) continue
      const abbr = doc.createElement('abbr')
      abbr.className = 'term'
      abbr.tabIndex = 0
      abbr.dataset.tip = definition
      const word = node.splitText(match.index)
      word.splitText(match[0].length)
      word.replaceWith(abbr)
      abbr.append(word)
      break
    }
  }
  return doc.body.innerHTML
}

// Content comes from our own API, so rendering it as HTML is safe.
function Markdown({ source, className = '' }) {
  const html = useMemo(() => addGlossary(marked.parse(source ?? '')), [source])
  return <div className={`prose ${className}`} dangerouslySetInnerHTML={{ __html: html }} />
}

export default Markdown
