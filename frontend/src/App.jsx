
import { useEffect, useState } from 'react'
import './App.css'

const API = 'http://127.0.0.1:8000'

function App() {
  const [repositories, setRepositories] = useState([])
  const [issues, setIssues] = useState([])
  const [repo, setRepo] = useState('Rahulsha9856/RepoFix-AI')
  const [issueId, setIssueId] = useState('3')
  const [loading, setLoading] = useState(false)
  const [apiOnline, setApiOnline] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadDashboard() {
      try {
        const [health, repoResponse, issueResponse] = await Promise.all([
          fetch(`${API}/`),
          fetch(`${API}/api/repositories/`),
          fetch(`${API}/api/issues`),
        ])

        setApiOnline(health.ok)

        if (repoResponse.ok) {
          const data = await repoResponse.json()
          const items = data.value || data
          setRepositories(Array.isArray(items) ? items : [])

          if (items.length > 0) {
            setRepo(
              items.find(r => r.full_name === repo)?.full_name ||
              items[0].full_name
            )
          }
        }

        if (issueResponse.ok) {
          const data = await issueResponse.json()
          const items = data.value || data
          setIssues(Array.isArray(items) ? items : [])

          if (items.length > 0) {
            setIssueId(
              String(items.find(i => i.id === 3)?.id || items[0].id)
            )
          }
        }
      } catch {
        setApiOnline(false)
      }
    }

    loadDashboard()
  }, [])

  async function runFix(event) {
    event.preventDefault()

    if (!issueId) {
      setError('Please select a database issue.')
      return
    }

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

  const fix = result?.fix_result
  const attempts = fix?.attempts || []
  const latestAttempt = attempts[attempts.length - 1]

  // Handle the three workflow states independently.
  const alreadyExists = result?.already_exists === true

  const passed =
    !alreadyExists &&
    result?.success === true &&
    fix?.success === true

  const failed = result && !alreadyExists && !passed

  const validationText = alreadyExists
    ? 'Already exists'
    : passed
      ? `${latestAttempt?.test_output?.match(/\d+ passed/)?.[0] || 'Passed'}`
      : failed
        ? 'Failed'
        : 'Not run'

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
          <span className={`status-dot ${apiOnline ? '' : 'offline'}`} />
          {apiOnline ? 'Backend connected' : 'Backend disconnected'}
          <small>API · localhost:8000</small>
        </div>
      </aside>

      <main className="main-content" id="dashboard">
        <header className="topbar">
          <div>
            <span className="eyebrow">REPOSITORY INTELLIGENCE</span>
            <h1>Code repair dashboard</h1>
          </div>

          <span className={`system-status ${apiOnline ? '' : 'offline-status'}`}>
            <span className={`status-dot ${apiOnline ? '' : 'offline'}`} />
            {apiOnline ? 'System online' : 'System offline'}
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
            <strong className={apiOnline ? 'green-text' : 'red-text'}>
              {apiOnline ? 'Running' : 'Offline'}
            </strong>
            <small>FastAPI service</small>
          </article>

          <article className="stat-card">
            <span>Current repository</span>
            <strong className="stat-repo">{repo || 'Not selected'}</strong>
            <small>GitHub repository</small>
          </article>

          <article className="stat-card">
            <span>Last validation</span>
            <strong
              className={
                alreadyExists || passed
                  ? 'green-text'
                  : failed
                    ? 'red-text'
                    : ''
              }
            >
              {validationText}
            </strong>
            <small>
              {result ? 'Latest execution' : 'Waiting for execution'}
            </small>
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
              <label htmlFor="repository">GitHub repository</label>
              <select
                id="repository"
                value={repo}
                onChange={event => setRepo(event.target.value)}
                required
              >
                {repositories.length === 0 && (
                  <option value={repo}>{repo}</option>
                )}

                {repositories.map(repository => (
                  <option key={repository.id} value={repository.full_name}>
                    {repository.full_name}
                  </option>
                ))}
              </select>

              <label htmlFor="issueId">Database issue</label>
              <select
                id="issueId"
                value={issueId}
                onChange={event => setIssueId(event.target.value)}
                required
              >
                {issues.length === 0 && (
                  <option value={issueId}>{issueId}</option>
                )}

                {issues.map(issue => (
                  <option key={issue.id} value={String(issue.id)}>
                    #{issue.number} — {issue.title} (DB ID: {issue.id})
                  </option>
                ))}
              </select>

              <p className="field-hint">
                Select the issue using its RepoFix database ID. The workflow
                uses the issue record to locate the target repository.
              </p>

              <button className="run-button" disabled={loading || !apiOnline}>
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

            {!result && !error && !loading && (
              <div className="empty-state">
                <div className="empty-icon">{'{ }'}</div>
                <strong>Waiting for a repair</strong>
                <p>Start a workflow to see its status and output here.</p>
              </div>
            )}

            {loading && (
              <div className="loading-state">
                <span className="spinner" />
                Running RepoFix AI workflow...
                <p>
                  Analyzing repository, generating patch and validating tests.
                </p>
              </div>
            )}

            {error && (
              <div className="error-result">
                <strong>Repair request failed</strong>
                <p>{error}</p>
                <small>Check the backend service and selected issue.</small>
              </div>
            )}

            {result && (
              <div className="result-content">
                <div
                  className={`repair-banner ${
                    alreadyExists || passed ? 'success' : 'failure'
                  }`}
                >
                  <strong>
                    {alreadyExists
                      ? '✓ Existing pull request found'
                      : passed
                        ? '✓ Repair successful'
                        : '✕ Repair failed'}
                  </strong>

                  <span>
                    {alreadyExists
                      ? result.message ||
                        'An open pull request already exists for this issue.'
                      : passed
                        ? 'Patch applied and validation completed.'
                        : `Workflow stage: ${result.stage || 'Unknown'}`}
                  </span>
                </div>

                <div className="result-metrics">
                  <div>
                    <span>Attempts</span>
                    <strong>{attempts.length}</strong>
                  </div>

                  <div>
                    <span>Validation</span>
                    <strong>
                      {alreadyExists
                        ? 'Not run'
                        : passed
                          ? 'Passed'
                          : 'Failed'}
                    </strong>
                  </div>

                  <div>
                    <span>Commit</span>
                    <strong>
                      {result.commit_sha ? 'Created' : 'Not created'}
                    </strong>
                  </div>
                </div>

                {result.branch && (
                  <div className="result-detail">
                    <span>Branch</span>
                    <code>{result.branch}</code>
                  </div>
                )}

                {result.pull_request?.branch && (
                  <div className="result-detail">
                    <span>PR branch</span>
                    <code>{result.pull_request.branch}</code>
                  </div>
                )}

                {result.commit_sha && (
                  <div className="result-detail">
                    <span>Commit SHA</span>
                    <code>{result.commit_sha}</code>
                  </div>
                )}

                {result.pull_request?.url && (
                  <a
                    className="pr-link"
                    href={result.pull_request.url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    View GitHub Pull Request #{result.pull_request.number} →
                  </a>
                )}

                {latestAttempt?.test_output && (
                  <div className="test-output">
                    <strong>Test output</strong>
                    <pre>{latestAttempt.test_output}</pre>
                  </div>
                )}

                {fix?.final_patch && (
                  <details className="patch-details">
                    <summary>View generated patch</summary>
                    <pre>{fix.final_patch}</pre>
                  </details>
                )}
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
