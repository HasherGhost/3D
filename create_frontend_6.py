import pathlib
ROOT = pathlib.Path(r"E:\3D")
C = ROOT / "app/frontend/src/components"
def w(name, content):
    (C / name).write_text(content, encoding="utf-8")
    print("  wrote", name)

# Detector.jsx -- the orchestrating section with state machine
w("Detector.jsx", """\
import React, { useState, useCallback } from 'react'
import UploadZone from './UploadZone.jsx'
import SampleRow  from './SampleRow.jsx'
import Result     from './Result.jsx'
import './Detector.css'

/*
 * State machine: idle -> loading -> result
 *                                -> error (bad file, network, server)
 *                idle <- (reset)
 */
function useDetector() {
  const [phase,    setPhase]    = useState('idle')   // idle|loading|result|error
  const [result,   setResult]   = useState(null)
  const [imageUrl, setImageUrl] = useState(null)
  const [errorMsg, setErrorMsg] = useState('')

  // Post a File to /predict and update state
  async function call(file) {
    const form = new FormData()
    form.append('file', file)
    const res = await fetch('/predict', { method: 'POST', body: form })
    if (!res.ok) {
      const body = await res.json().catch(() => ({}))
      throw new Error(body.detail ?? 'Server error ' + res.status)
    }
    return res.json()
  }

  // Run on a local File object (from upload or paste)
  const runFile = useCallback(async (file, validErr) => {
    if (validErr === 'wrong-type') {
      setErrorMsg('Please upload a jpg, png, or webp image.')
      setPhase('error'); return
    }
    if (validErr === 'too-large') {
      setErrorMsg('The file is larger than 10 MB. Please try a smaller image.')
      setPhase('error'); return
    }
    const url = URL.createObjectURL(file)
    setImageUrl(prev => { if (prev) URL.revokeObjectURL(prev); return url })
    setPhase('loading')
    setResult(null)
    try {
      setResult(await call(file))
      setPhase('result')
    } catch (err) {
      setErrorMsg(err.message ?? 'Something went wrong. Try another image.')
      setPhase('error')
    }
  }, [])

  // Run on a sample URL (fetch as blob first, then post)
  const runSample = useCallback(async (sampleUrl, filename) => {
    setImageUrl(sampleUrl)
    setPhase('loading')
    setResult(null)
    try {
      const blobRes = await fetch(sampleUrl)
      if (!blobRes.ok) throw new Error('Sample image not found on server.')
      const blob = await blobRes.blob()
      const file = new File([blob], filename, { type: blob.type })
      setResult(await call(file))
      setPhase('result')
    } catch (err) {
      setErrorMsg(err.message ?? 'Could not load the sample.')
      setPhase('error')
    }
  }, [])

  const reset = useCallback(() => {
    setPhase('idle')
    setResult(null)
    setErrorMsg('')
  }, [])

  return { phase, result, imageUrl, errorMsg, runFile, runSample, reset }
}

export default function Detector() {
  const { phase, result, imageUrl, errorMsg, runFile, runSample, reset } = useDetector()

  return (
    <section id="detector" className="section">
      <div className="container detector">
        <span className="label">Detector</span>

        {/* Upload zone: visible when idle or on error */}
        {(phase === 'idle' || phase === 'error') && (
          <>
            <UploadZone onFile={runFile} />
            <SampleRow  onSample={runSample} />
          </>
        )}

        {/* Loading state */}
        {phase === 'loading' && (
          <div className="detector__loading" aria-live="polite" aria-busy="true">
            <div className="detector__progress" role="progressbar" aria-label="Analyzing image" />
            <p>Analyzing\u2026</p>
          </div>
        )}

        {/* Error state */}
        {phase === 'error' && (
          <p className="detector__error" role="alert">{errorMsg}</p>
        )}

        {/* Result state */}
        {phase === 'result' && result && (
          <Result imageUrl={imageUrl} data={result} />
        )}

        {/* Reset button -- shown after any non-idle state */}
        {phase !== 'idle' && (
          <button className="detector__reset" onClick={reset}>
            {phase === 'loading' ? 'Cancel' : 'Analyze another image'}
          </button>
        )}
      </div>
    </section>
  )
}
""")

# Detector.css
w("Detector.css", """\
.detector {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.detector > .label {
  display: block;
  margin-bottom: 2rem;
}

/* -- Loading state -------------------------------------------------------- */
.detector__loading {
  margin-top: 2.5rem;
  color: var(--text-secondary);
  font-size: 15px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* Thin animated progress line -- no spinner, no gif */
.detector__progress {
  height: 1px;
  background: var(--hairline);
  position: relative;
  overflow: hidden;
}

.detector__progress::after {
  content: '';
  position: absolute;
  top: 0; left: -50%;
  width: 50%;
  height: 100%;
  background: var(--accent);
  animation: sweep 1.1s ease-in-out infinite;
}

@keyframes sweep {
  from { left: -50%; }
  to   { left: 110%; }
}

/* -- Error state ---------------------------------------------------------- */
.detector__error {
  margin-top: 1rem;
  color: var(--text);
  max-width: 55ch;
}

/* -- Reset button --------------------------------------------------------- */
.detector__reset {
  margin-top: 2.5rem;
  align-self: flex-start;
  border: 1px solid var(--hairline);
  border-radius: 4px;
  padding: 0.5rem 1.25rem;
  font-size: 15px;
  color: var(--text-secondary);
  transition: border-color 150ms ease, color 150ms ease;
}

.detector__reset:hover {
  border-color: var(--accent);
  color: var(--accent);
}
""")

print("Detector done.")
