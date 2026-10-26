import React from 'react'
import './Hero.css'

/* Editorial hero: large serif headline, restrained accent, and plain language. */
export default function Hero() {
  return (
    <section id="hero" className="section section--hero">
      <div className="container hero">
        <h1 className="hero__headline">
          Is this image <em>real?</em>
        </h1>
        <p className="hero__sub">
          Upload an image and our model will estimate whether it looks real
          or AI-generated. One model. Plain numbers.
        </p>
      </div>
    </section>
  )
}
