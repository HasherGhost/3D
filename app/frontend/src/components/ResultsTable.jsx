import React from 'react'
import './ResultsTable.css'

const METRICS = [
  { name: 'Accuracy',  value: '98.88%' },
  { name: 'Precision', value: '98.56%' },
  { name: 'Recall',    value: '99.20%' },
  { name: 'F1-score',  value: '98.88%' },
  { name: 'ROC-AUC',   value: '0.9994' },
]

export default function ResultsTable() {
  return (
    <section id="results" className="section">
      <div className="container res">
        <span className="label">Results</span>
        <table className="res__table">
          <caption className="res__caption">
            Held-out test set, 20,000 images. Fake = positive class.
          </caption>
          <thead>
            <tr>
              <th scope="col">Metric</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody>
            {METRICS.map(m => (
              <tr key={m.name}>
                <td>{m.name}</td>
                <td>{m.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
