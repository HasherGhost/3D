import React from 'react'
import './Result.css'

/* Result panel: image on the left, verdict + metric on the right.
   Reveals with a short opacity + translate fade. */
export default function Result({ imageUrl, data }) {
  const { p_ai, label } = data
  const isAI   = label === 'ai'
  const pct    = Math.round(p_ai * 100)
  const display = pct > 99 ? '>99%' : pct + '%'

  return (
    <div className="result" role="region" aria-label="Detection result">
      {/* Image preview at its natural aspect ratio */}
      <div className="result__img-wrap">
        <img src={imageUrl} alt="Analyzed portrait" className="result__img" />
      </div>

      {/* Analysis */}
      <div className="result__analysis">
        <p className={isAI ? 'result__verdict result__verdict--ai'
                           : 'result__verdict result__verdict--real'}>
          {isAI ? 'Likely AI-generated.' : 'Likely a real photograph.'}
        </p>

        <div className="result__metric">
          <span className="result__big-num" aria-label={display + ' probability AI-generated'}>
            {display}
          </span>
          <span className="label result__pct-label">probability AI-generated</span>
        </div>

        {/* 2px horizontal bar */}
        <div
          className="result__track"
          role="progressbar"
          aria-valuenow={pct}
          aria-valuemin={0}
          aria-valuemax={100}
        >
          <div
            className="result__fill"
            style={{ width: Math.min(p_ai * 100, 100) + '%' }}
          />
        </div>

        <p className="result__disclaimer">
          One model, trained on StyleGAN faces.{' '}
          <a href="#limits">See Limits.</a>
        </p>
      </div>
    </div>
  )
}
