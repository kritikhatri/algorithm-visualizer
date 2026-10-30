import { Link } from 'react-router-dom'
import { useApi } from '../useApi'

function CheatSheet() {
  const { data, error } = useApi('/cheatsheet')

  return (
    <>
      <header className="page-header">
        <p className="eyebrow">Quick reference</p>
        <h1>Complexity cheat sheet</h1>
        <p className="subtitle left">The Big-O of every operation covered on this site, in one page.</p>
        <Link className="button ghost small header-link" to="/patterns">Test yourself: which technique fits? →</Link>
      </header>
      {error && <p className="card error-text">{error.message}</p>}
      <div className="cheat-grid">
        {(data?.topics ?? []).map((topic) => (
          <section className="card" key={topic.id}>
            <h2 className="card-title"><Link to={`/topics/${topic.id}`}>{topic.title}</Link></h2>
            <table className="complexity-table">
              <thead><tr><th>Operation</th><th>Time</th><th>Space</th></tr></thead>
              <tbody>
                {topic.complexity.map((row) => (
                  <tr key={row.operation}>
                    <td>{row.operation}</td>
                    <td><code>{row.time}</code></td>
                    <td><code>{row.space}</code></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
        ))}
      </div>
    </>
  )
}

export default CheatSheet
