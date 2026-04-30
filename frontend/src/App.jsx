import { useState } from 'react'
import ReportViewer from './components/ReportViewer'
import { getApiBase } from './config'

function App() {
  const API_BASE = getApiBase();

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    email: '',
    dob: ''
  })
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)
  const [progress, setProgress] = useState({ value: 0, message: '' })

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    setLoading(true)
    setResults({ profiles: [], breaches: [] })
    setProgress({ value: 0, message: 'Свързване със сървъра...' })

    try {
      const params = new URLSearchParams(formData).toString()
      const response = await fetch(`${API_BASE}/api/search/stream?${params}`)

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      let buffer = ''
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop()

        for (const line of lines) {
          if (!line.trim()) continue
          const event = JSON.parse(line)

          if (event.type === 'progress') {
            setProgress({ value: event.value, message: event.message })
          } else if (event.type === 'breaches') {
            setResults(prev => ({ ...prev, breaches: event.data }))
          } else if (event.type === 'profile') {
            setResults(prev => ({ ...prev, profiles: [...prev.profiles, event.data] }))
          } else if (event.type === 'done') {
            setResults({ profiles: event.profiles, breaches: event.breaches })
          }
        }
      }
    } catch (error) {
      console.error("Search failed:", error)
      alert(`Грешка: ${error.message}\nОпитах адрес: ${API_BASE}\nВашият порт е: ${window.location.port || 'няма'}\nПроверете дали Python сървърът работи!`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Breacherr</h1>
      <p className="subtitle">Вашият персонален инструмент за OSINT и проверка за изтичане на данни</p>

      <div className="glass-card">
        <form onSubmit={handleSearch}>
          <div className="results-grid" style={{ marginTop: 0, gap: '1rem' }}>
            <div className="form-group">
              <label>Име</label>
              <input
                type="text"
                name="first_name"
                placeholder="Иван"
                value={formData.first_name}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label>Фамилия</label>
              <input
                type="text"
                name="last_name"
                placeholder="Иванов"
                value={formData.last_name}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Потребителско име (Username)</label>
            <input
              type="text"
              name="username"
              placeholder="ivan_ivanov88"
              value={formData.username}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Имейл адрес (за проверка на breaches)</label>
            <input
              type="email"
              name="email"
              placeholder="ivan@example.com"
              value={formData.email}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Дата на раждане</label>
            <input
              type="date"
              name="dob"
              value={formData.dob}
              onChange={handleChange}
            />
          </div>

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Сканиране...' : 'Започни сканиране'}
          </button>
        </form>
      </div>

      {loading && (
        <div className="progress-container">
          <div className="progress-bar-wrapper">
            <div
              className="progress-bar-fill"
              style={{ width: `${progress.value}%` }}
            ></div>
          </div>
          <p className="progress-text">{progress.message}</p>
        </div>
      )}

      {results && (results.profiles.length > 0 || results.breaches.length > 0) && (
        <ReportViewer results={results} searchData={formData} />
      )}
    </div>
  )
}

export default App
