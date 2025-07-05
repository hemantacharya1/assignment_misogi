import React, { useState } from 'react'
import './App.css'

function App() {
  const [texts, setTexts] = useState(['', '', '', ''])
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleTextChange = (index, value) => {
    const newTexts = [...texts]
    newTexts[index] = value
    setTexts(newTexts)
  }

  const handleAnalyze = async () => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          texts: texts.filter(text => text.trim() !== '')
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Analysis failed')
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleClear = () => {
    setTexts(['', '', '', ''])
    setResults(null)
    setError(null)
  }

  const renderSimilarityMatrix = () => {
    if (!results) return null

    const matrix = results.similarity_matrix
    const nonEmptyTexts = texts.filter(text => text.trim() !== '')

    return (
      <div className="results-section">
        <h3>Similarity Matrix</h3>
        <div className="matrix-container">
          <table className="similarity-matrix">
            <thead>
              <tr>
                <th></th>
                {nonEmptyTexts.map((_, index) => (
                  <th key={index}>Text {index + 1}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {matrix.map((row, i) => (
                <tr key={i}>
                  <td className="row-header">Text {i + 1}</td>
                  {row.map((similarity, j) => (
                    <td 
                      key={j} 
                      className={`similarity-cell ${
                        i !== j && similarity >= 80 ? 'high-similarity' : ''
                      }`}
                    >
                      {similarity.toFixed(1)}%
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="summary">
          <h4>Analysis Summary</h4>
          <p>Threshold: {results.threshold_percentage}%</p>
          <p>Highest Similarity: {(results.highest_similarity * 100).toFixed(1)}%</p>
          
          {results.flagged_pairs.length > 0 && (
            <div className="flagged-pairs">
              <h4>🚨 Potential Plagiarism Detected</h4>
              {results.flagged_pairs.map((pair, index) => (
                <div key={index} className="flagged-pair">
                  <strong>Text {pair.text1_index + 1} ↔ Text {pair.text2_index + 1}</strong>: 
                  {pair.similarity_percentage.toFixed(1)}% similarity
                </div>
              ))}
            </div>
          )}
          
          {results.flagged_pairs.length === 0 && (
            <div className="no-plagiarism">
              <p>✅ No potential plagiarism detected</p>
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🔍 Plagiarism Detector</h1>
        <p>Semantic similarity analysis using HuggingFace embeddings</p>
      </header>

      <main className="app-main">
        <div className="input-section">
          <h2>Enter Texts to Compare</h2>
          <p className="instruction">Enter 2-4 texts to analyze for potential plagiarism</p>
          
          <div className="text-inputs">
            {texts.map((text, index) => (
              <div key={index} className="text-input-group">
                <label htmlFor={`text-${index}`}>Text {index + 1}:</label>
                <textarea
                  id={`text-${index}`}
                  value={text}
                  onChange={(e) => handleTextChange(index, e.target.value)}
                  placeholder={`Enter text ${index + 1}...`}
                  rows="4"
                />
              </div>
            ))}
          </div>

          <div className="action-buttons">
            <button 
              onClick={handleAnalyze} 
              disabled={loading || texts.filter(t => t.trim()).length < 2}
              className="analyze-button"
            >
              {loading ? 'Analyzing...' : 'Analyze Texts'}
            </button>
            <button onClick={handleClear} className="clear-button">
              Clear All
            </button>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {renderSimilarityMatrix()}
      </main>
    </div>
  )
}

export default App 