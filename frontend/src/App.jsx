
import { useState } from 'react'
import './App.css'

const API = 'http://127.0.0.1:8000'

function App() {
  const [repo, setRepo] = useState('Rahulsha9856/RepoFix-AI')
  const [issueId, setIssueId] = useState('3')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  async function runFix(event) {
    event.preventDefault()
    setLoading(true)
    setResult(null)
    setError('')

    try {
      const response = await fetch(
        `${API}/api/fix-attempts/run/${issueId}`,
        { method: 'POST' }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Fix attempt failed')
      }

      setResult(data)
    } catch (err) {
      setError(err.message || 'Could not connect to RepoFix AI backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">RF</div>
          <div>
            <strong>RepoFix AI</strong>
            <span>Autonomous code repair</span>
          </div>
        </div>

        <nav>
          <a className="nav-item active" href="#dashboard">Dashboard</a>
          <a className="nav-item" href="#run-fix">Run a fix</a>
          <a className="nav-item" href="#results">Results</a>
        </nav>

        <div className="sidebar-bottom">
          <span className="status-dot" />
          Backend connected
          <small>API · localhost:8000</small>
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div>
            <span className="eyebrow">REPOSITORY INTELLIGENCE</span>
            <h1>Code repair dashboard</h1>
          </div>
          <span className="system-status">
            <span className="status-dot" /> System online
          </span>
        </header>

        <section className="welcome-card">
          <div>
            <span className="eyebrow">AI-POWERED REPAIR</span>
            <h2>Fix bugs. Validate automatically.</h2>
            <p>
              Analyze repository issues, generate code patches, and run tests
              through your RepoFix AI workflow.
            </p>
          </div>
          <div className="welcome-symbol">{'{ }'}</div>
        </section>

        <section className="stats-grid">
          <article className="stat-card">
            <span>Backend status</span>
            <strong className="green-text">Running</strong>
            <small>FastAPI service</small>
          </article>
          <article className="stat-card">
            <span>Current repository</span>
            <strong className="stat-repo">{repo || 'Not selected'}</strong>
            <small>GitHub repository</small>
          </article>
          <article className="stat-card">
            <span>Last validation</span>
            <strong className="green-text">1 passed</strong>
            <small>Previously verified test</small>
          </article>
        </section>

        <section className="workspace-grid">
          <article className="panel" id="run-fix">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">WORKFLOW</span>
                <h2>Start a repair</h2>
              </div>
              <span className="step-badge">01</span>
            </div>

            <form onSubmit={runFix}>
              <label htmlFor="repository">Repository full name</label>
              <input
                id="repository"
                value={repo}
                onChange={(event) => setRepo(event.target.value)}
                placeholder="owner/repository"
                required
              />

              <label htmlFor="issueId">Database issue ID</label>
              <input
                id="issueId"
                type="number"
                min="1"
                value={issueId}
                onChange={(event) => setIssueId(event.target.value)}
                required
              />

              <p className="field-hint">
                Enter the RepoFix database issue ID, not the GitHub issue number.
              </p>

              <button className="run-button" disabled={loading}>
                {loading ? 'Repair running...' : 'Run automated fix'}
                <span>→</span>
              </button>
            </form>
          </article>

          <article className="panel" id="results">
            <div className="panel-heading">
              <div>
                <span className="eyebrow">EXECUTION OUTPUT</span>
                <h2>Repair results</h2>
              </div>
              <span className="step-badge">02</span>
            </div>

            {!result && !error && (
              <div className="empty-state">
                <div className="empty-icon">⌘</div>
                <strong>Waiting for a repair</strong>
                <p>Start a workflow to see its status and output here.</p>
              </div>
            )}

            {loading && (
              <div className="loading-state">
                <span className="spinner" />
                Running RepoFix AI workflow...
              </div>
            )}

            {error && (
              <div className="error-result">
                <strong>Repair request failed</strong>
                <p>{error}</p>
                <small>Check that the backend is running and the issue ID exists.</small>
              </div>
            )}

            {result && (
              <div className="result-content">
                <div className="result-status">
                  <span className="status-dot" />
                  Workflow response received
                </div>
                <pre>{JSON.stringify(result, null, 2)}</pre>
              </div>
            )}
          </article>
        </section>

        <footer>
          RepoFix AI <span>·</span> Intelligent repository repair
        </footer>
      </main>
    </div>
  )
}

export default App
