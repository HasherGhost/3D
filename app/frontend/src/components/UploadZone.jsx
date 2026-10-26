import React, { useCallback, useEffect, useRef, useState } from 'react'
import './UploadZone.css'

const ACCEPTED  = ['image/jpeg', 'image/png', 'image/webp']
const MAX_BYTES = 10 * 1024 * 1024   // 10 MB

/* Large rectangle drop zone. Supports drag-and-drop, click, and paste.
   Calls onFile(file, error) where error is null on success. */
export default function UploadZone({ onFile }) {
  const [dragging, setDragging] = useState(false)
  const inputRef  = useRef(null)

  const validate = useCallback((file) => {
    if (!file) return
    if (!ACCEPTED.includes(file.type)) { onFile(null, 'wrong-type'); return }
    if (file.size > MAX_BYTES)          { onFile(null, 'too-large');  return }
    onFile(file, null)
  }, [onFile])

  const open = () => inputRef.current?.click()

  const onKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open() }
  }

  const onDragOver  = (e) => { e.preventDefault(); setDragging(true) }
  const onDragLeave = ()  => setDragging(false)
  const onDrop      = (e) => { e.preventDefault(); setDragging(false); validate(e.dataTransfer.files[0]) }

  // Global paste handler
  useEffect(() => {
    const onPaste = (e) => {
      const item = [...(e.clipboardData?.items ?? [])].find(i => i.kind === 'file')
      if (item) validate(item.getAsFile())
    }
    window.addEventListener('paste', onPaste)
    return () => window.removeEventListener('paste', onPaste)
  }, [validate])

  return (
    <div
      className={dragging ? 'upload-zone upload-zone--over' : 'upload-zone'}
      role="button"
      tabIndex={0}
      aria-label="Upload image. Drop a file, click to browse, or paste from clipboard."
      onClick={open}
      onKeyDown={onKeyDown}
      onDragOver={onDragOver}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
    >
      <span className="upload-zone__main">Drop an image here, or choose a file</span>
      <span className="upload-zone__hint">jpg · png · webp · max 10 MB · or paste from clipboard</span>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        aria-hidden="true"
        tabIndex={-1}
        style={{ display: 'none' }}
        onChange={(e) => validate(e.target.files[0])}
      />
    </div>
  )
}
