import { useMemo } from 'react'
import CodeMirror from '@uiw/react-codemirror'
import { python } from '@codemirror/lang-python'
import { oneDark } from '@codemirror/theme-one-dark'
import { Decoration, EditorView } from '@codemirror/view'

const theme = EditorView.theme({
  '&': { backgroundColor: 'transparent', fontSize: '13.5px' },
  '.cm-gutters': { backgroundColor: 'transparent', border: 'none' },
  '.cm-scroller': { fontFamily: 'var(--mono)', lineHeight: '1.6' },
  '.cm-step-line': {
    backgroundColor: 'rgba(255, 79, 163, 0.16)',
    boxShadow: 'inset 3px 0 0 var(--pink)',
  },
})

function highlightLine(line) {
  return EditorView.decorations.compute([], (state) => {
    if (!line || line > state.doc.lines) return Decoration.none
    return Decoration.set([
      Decoration.line({ class: 'cm-step-line' }).range(state.doc.line(line).from),
    ])
  })
}

function CodeEditor({ value, onChange, readOnly = false, activeLine, minHeight, maxHeight }) {
  const extensions = useMemo(
    () => [python(), theme, EditorView.lineWrapping, highlightLine(activeLine)],
    [activeLine]
  )

  return (
    <div className={`code-editor ${readOnly ? 'read-only' : ''}`}>
      <CodeMirror
        value={value}
        onChange={onChange}
        theme={oneDark}
        extensions={extensions}
        editable={!readOnly}
        readOnly={readOnly}
        minHeight={minHeight}
        maxHeight={maxHeight}
        basicSetup={{
          foldGutter: false,
          highlightActiveLine: !readOnly,
          highlightActiveLineGutter: !readOnly,
        }}
      />
    </div>
  )
}

export default CodeEditor
