import React from 'react'
import './Footer.css'

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <p className="footer__names">
          [Your Name] · [Team Member] · [Team Member]
          <span className="footer__sep">—</span>
          [Your College Name]
        </p>
        <p className="footer__note">
          Final-year project, 2024–25. Model weights are not distributed.
        </p>
      </div>
    </footer>
  )
}
