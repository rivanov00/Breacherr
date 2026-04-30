import React from 'react'
import { getApiBase } from '../config'

function ReportViewer({ results, searchData }) {
  const API_BASE = getApiBase();

  const handleExport = async (format) => {
    try {
      //const response = await fetch(`http://localhost:8000/api/export?format=${format}`, {
      const response = await fetch(`${API_BASE}/api/export?format=${format}`, {

        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(searchData)
      })
      const data = await response.json()

      // Create a download link for the exported data
      const blob = new Blob([data.data], { type: format === 'json' ? 'application/json' : 'text/xml' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `breacherr_report.${format}`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error("Export failed:", error)
      alert("Грешка при експортирането.")
    }
  }

  return (
    <div className="results-container">
      <div className="results-grid">
        {/* Social Profiles Section */}
        <div className="glass-card">
          <h2 className="section-title">
            <span>🌐</span> Социални профили
          </h2>
          {results.profiles.length > 0 ? (
            Object.entries(
              results.profiles.reduce((acc, p) => {
                const score = p.match_score || 0;
                if (!acc[p.platform]) acc[p.platform] = { icon: p.icon, links: [], max_score: 0 };
                acc[p.platform].links.push({ url: p.url, score: score });
                if (score > acc[p.platform].max_score) acc[p.platform].max_score = score;
                return acc;
              }, {})
            )
              .sort((a, b) => b[1].max_score - a[1].max_score)
              .map(([platform, data], index) => {
                const globalMaxScore = Math.max(...results.profiles.map(p => p.match_score || 0));

                return (
                  <div key={index} className="platform-card" style={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                        <img src={data.icon} alt={platform} style={{ width: '24px', height: '24px', borderRadius: '4px' }} />
                        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{platform}</div>
                      </div>
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <span className="badge badge-success">Намерен</span>
                      </div>
                    </div>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem', width: '100%', marginTop: '0.5rem' }}>
                      {data.links
                        .sort((a, b) => b.score - a.score)
                        .map((link, i) => (
                          <div key={i} className="profile-link-row">
                            <a href={link.url} target="_blank" rel="noreferrer" className="profile-url">
                              {link.url}
                            </a>
                            <span className="profile-score" style={{ color: link.score >= 90 ? 'var(--accent)' : 'var(--text-muted)' }}>
                              {(link.score || 0)}% съвпадение
                            </span>
                          </div>
                        ))}
                    </div>
                  </div>
                );
              })
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>Не бяха открити публични профили.</p>
          )}
        </div>

        {/* Data Breaches Section */}
        <div className="glass-card">
          <h2 className="section-title">
            <span>🛡️</span> Изтичане на данни
          </h2>
          {results.breaches.length > 0 ? (
            results.breaches.map((breach, index) => (
              <div key={index} className="breach-card">
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-start' }}>
                  {breach.Avatar && (
                    <img src={breach.Avatar} alt="Profile" className="breach-avatar" />
                  )}
                  <div style={{ flex: 1 }}>
                    <div className="breach-name">{breach.Title}</div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--accent)', marginBottom: '0.5rem' }}>
                      Източник: {breach.Name} ({breach.Domain})
                    </div>
                    <div className="breach-date">Дата на изтичане: {breach.BreachDate}</div>
                    <div className="breach-desc">{breach.Description}</div>
                  </div>
                </div>

                {breach.SecurityAnalysis && (
                  <div className="security-panel">
                    <div className="security-header">
                      <span>🔐</span> Сигурност на паролата: <strong>{breach.SecurityAnalysis.label}</strong>
                    </div>
                    <div className="security-progress">
                      <div
                        className={`security-bar security-score-${breach.SecurityAnalysis.score}`}
                        style={{ width: `${(breach.SecurityAnalysis.score + 1) * 20}%` }}
                      ></div>
                    </div>
                    <p style={{ fontSize: '0.85rem', margin: '0.5rem 0' }}>
                      Време за разбиване: <strong>{breach.SecurityAnalysis.crack_time}</strong>
                    </p>
                    {breach.SecurityAnalysis.feedback.length > 0 && (
                      <ul className="security-feedback">
                        {breach.SecurityAnalysis.feedback.map((f, i) => <li key={i}>{f}</li>)}
                      </ul>
                    )}
                    <div className="password-snippet">
                      Разкрита парола: <code>{breach.PasswordSnippet}</code>
                    </div>
                  </div>
                )}

                <div style={{ marginTop: '0.5rem', fontSize: '0.8rem' }}>
                  <strong>Компрометирани данни:</strong> {breach.DataClasses.join(', ')}
                </div>
              </div>
            ))
          ) : (
            <p style={{ color: 'var(--text-muted)' }}>Няма открити данни за изтичане на информация за този имейл.</p>
          )}
        </div>
      </div>

      <div className="export-buttons">
        <button className="btn-secondary" onClick={() => handleExport('json')}>
          Експорт в JSON
        </button>
        <button className="btn-secondary" onClick={() => handleExport('xml')}>
          Експорт в XML
        </button>
      </div>
    </div>
  )
}

export default ReportViewer
