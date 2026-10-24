import { Link } from 'react-router-dom'

function NotFound() {
  return (
    <section className="card empty-state">
      <h1>Page not found</h1>
      <p className="muted">That page doesn't exist, but there's plenty to learn elsewhere.</p>
      <Link className="button primary" to="/">Back to topics</Link>
    </section>
  )
}

export default NotFound
