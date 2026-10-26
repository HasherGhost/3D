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
