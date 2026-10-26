import pathlib
ROOT = pathlib.Path(r"E:\3D")
C = ROOT / "app/frontend/src/components"
def w(name, content):
    (C / name).write_text(content, encoding="utf-8")
    print("  wrote", name)

# UploadZone.jsx
w("UploadZone.jsx", """\
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
""")

# UploadZone.css
w("UploadZone.css", """\
.upload-zone {
  border: 1px solid var(--hairline);
  border-radius: 4px;
  padding: 3.5rem 2rem;
  text-align: center;
  cursor: pointer;
  user-select: none;
  transition: border-color 150ms ease, background 150ms ease;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.upload-zone:hover,
.upload-zone--over {
  border-color: var(--accent);
  background: rgba(180, 83, 42, 0.025);
}

.upload-zone__main {
  font-size: 17px;
  color: var(--text);
}

.upload-zone__hint {
  font-size: 13px;
  color: var(--text-secondary);
}

@media (max-width: 480px) {
  .upload-zone { padding: 2.5rem 1.25rem; }
}
""")

# SampleRow.jsx
w("SampleRow.jsx", """\
import React from 'react'
import './SampleRow.css'

/* Six small thumbnails. Clicking one runs the detector on that sample image. */
const SAMPLES = [
  { name: '1.jpg', alt: 'Sample portrait 1' },
  { name: '2.jpg', alt: 'Sample portrait 2' },
  { name: '3.jpg', alt: 'Sample portrait 3' },
  { name: '4.jpg', alt: 'Sample portrait 4' },
  { name: '5.jpg', alt: 'Sample portrait 5' },
  { name: '6.jpg', alt: 'Sample portrait 6' },
]

export default function SampleRow({ onSample }) {
  return (
    <div className="sample-row">
      <span className="label">Or try an example</span>
      <ul className="sample-row__list" role="list">
        {SAMPLES.map(s => (
          <li key={s.name}>
            <button
              className="sample-row__thumb"
              onClick={() => onSample('/samples/' + s.name, s.name)}
              aria-label={'Run detector on ' + s.alt}
            >
              <img
                src={'/samples/' + s.name}
                alt={s.alt}
                width={56}
                height={56}
                loading="lazy"
                onError={(e) => { e.currentTarget.parentElement.style.opacity = '0.25' }}
              />
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
""")

# SampleRow.css
w("SampleRow.css", """\
.sample-row {
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.sample-row__list {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  list-style: none;
}

.sample-row__thumb {
  width: 56px;
  height: 56px;
  border: 1px solid var(--hairline);
  border-radius: 4px;
  overflow: hidden;
  padding: 0;
  transition: border-color 150ms ease;
}

.sample-row__thumb:hover {
  border-color: var(--accent);
}

.sample-row__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
""")

print("UploadZone + SampleRow done.")
