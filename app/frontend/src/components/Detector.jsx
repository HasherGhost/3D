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
            <p>Analyzing…</p>
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
