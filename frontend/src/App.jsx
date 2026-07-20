import { useState } from 'react'
import { predictSurvival } from './api.js'

const initialForm = {
  pclass: '3',
  sex: 'male',
  age: '',
  fare: '',
  embarked: '',
}

function App() {
  const [form, setForm] = useState(initialForm)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  function handleChange(event) {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setResult(null)
    setError(null)

    const payload = {
      pclass: Number(form.pclass),
      sex: form.sex,
      fare: Number(form.fare),
    }
    if (form.age !== '') payload.age = Number(form.age)
    if (form.embarked !== '') payload.embarked = form.embarked

    try {
      const data = await predictSurvival(payload)
      setResult(data)
    } catch (err) {
      setError(err.message || 'Something went wrong. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <div className="card">
        <h1>Titanic Survival Prediction</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Ticket class
            <select name="pclass" value={form.pclass} onChange={handleChange}>
              <option value="1">1st</option>
              <option value="2">2nd</option>
              <option value="3">3rd</option>
            </select>
          </label>

          <label>
            Sex
            <select name="sex" value={form.sex} onChange={handleChange}>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </label>

          <label>
            Age (optional)
            <input
              type="number"
              name="age"
              min="0"
              max="120"
              step="1"
              value={form.age}
              onChange={handleChange}
              placeholder="e.g. 32"
            />
          </label>

          <label>
            Fare
            <input
              type="number"
              name="fare"
              min="0"
              step="0.01"
              required
              value={form.fare}
              onChange={handleChange}
              placeholder="e.g. 7.25"
            />
          </label>

          <label>
            Port of embarkation (optional)
            <select name="embarked" value={form.embarked} onChange={handleChange}>
              <option value="">Unknown</option>
              <option value="S">Southampton</option>
              <option value="C">Cherbourg</option>
              <option value="Q">Queenstown</option>
            </select>
          </label>

          <button type="submit" disabled={loading}>
            {loading ? 'Predicting…' : 'Predict'}
          </button>
        </form>

        {error && <p className="result error">{error}</p>}

        {result && (
          <p className={`result ${result.survived ? 'survived' : 'not-survived'}`}>
            {result.survived
              ? `Survived ✅ (${Math.round(result.survival_probability * 100)}% confidence)`
              : `Did not survive ❌ (${Math.round((1 - result.survival_probability) * 100)}% confidence)`}
          </p>
        )}
      </div>
    </div>
  )
}

export default App
