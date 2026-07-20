// note: we could also store the api url as an environment variable
const API_URL = 'https://titanic-survival-api-yafk.onrender.com/predict'

/**
 * Sends passenger features to the Titanic survival prediction API.
 * @param {object} payload - PassengerFeatures shaped object (pclass, sex, age?, fare, embarked?)
 * @returns {Promise<{survived: number, survival_probability: number}>}
 */
export async function predictSurvival(payload) {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(`Request failed (${response.status}): ${detail}`)
  }

  return response.json()
}
