import React, { useEffect, useState } from 'react'
import './Nav.css'

/* Top navigation: serif wordmark on the left, plain text links on the right.
   A hairline border appears under the nav once the user scrolls. */
export default function Nav() {
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  return (
    <header className={scrolled ? 'nav nav--scrolled' : 'nav'}>
      <div className="container nav__inner">
        <a href="#hero" className="nav__wordmark" aria-label="Lens home">
          Lens
        </a>
        <nav aria-label="Site navigation">
          <ul className="nav__links" role="list">
            <li><a href="#detector">Detector</a></li>
            <li><a href="#how-it-works">How it works</a></li>
            <li><a href="#results">Results</a></li>
            <li><a href="#limits">Limits</a></li>
          </ul>
        </nav>
      </div>
    </header>
  )
}
