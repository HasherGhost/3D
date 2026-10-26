import pathlib
ROOT = pathlib.Path(r"E:\3D")
C = ROOT / "app/frontend/src/components"
def w(name, content):
    (C / name).write_text(content, encoding="utf-8")
    print("  wrote", name)

# Result.jsx
w("Result.jsx", """\
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
""")

# Result.css
w("Result.css", """\
/* Reveal animation on result appearance */
@keyframes reveal {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0);   }
}

.result {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: start;
  animation: reveal 180ms ease both;
  margin-top: 3rem;
}

/* One very faint shadow on the image, nothing else */
.result__img-wrap {
  border-radius: 4px;
  overflow: hidden;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.07);
}

.result__img {
  width: 100%;
  height: auto;
  display: block;
}

.result__analysis {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.result__verdict {
  font-family: var(--font-serif);
  font-size: 1.6rem;
  font-weight: 400;
  line-height: 1.2;
}

.result__verdict--ai   { color: var(--accent); }
.result__verdict--real { color: var(--text);   }

.result__metric {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.result__big-num {
  font-family: var(--font-serif);
  font-size:   clamp(3rem, 6vw, 4.5rem);
  line-height: 1;
  color: var(--text);
}

/* Thin 2px bar */
.result__track {
  height: 2px;
  background: var(--hairline);
  border-radius: 1px;
  overflow: hidden;
}

.result__fill {
  height: 100%;
  background: var(--accent);
  border-radius: 1px;
  transition: width 300ms ease;
}

.result__disclaimer {
  font-size: 13px;
  color: var(--text-secondary);
}

.result__disclaimer a {
  color: var(--accent);
  text-decoration: underline;
  text-underline-offset: 2px;
}

@media (max-width: 620px) {
  .result {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
""")

print("Result done.")
