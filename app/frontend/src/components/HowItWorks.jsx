import React from 'react'
import './HowItWorks.css'

const STEPS = [
  {
    num:   '01',
    title: 'Starting from ImageNet',
    body:  'We take ResNet-50, pretrained on ImageNet’s 1.2 million photographs, as our backbone. Its early layers already detect edges, textures, and colour patterns — all useful for spotting the statistical fingerprints that GANs leave behind.',
  },
  {
    num:   '02',
    title: 'Two-stage fine-tuning',
    body:  'In the first stage we freeze the backbone and train only the final binary classifier — real or generated — for a few epochs. In the second stage we unfreeze the last residual block and fine-tune at a lower learning rate, letting the network adjust its highest-level features to this specific task.',
  },
  {
    num:   '03',
    title: 'Evaluation on held-out data',
    body:  'Before reporting any numbers we set aside 20,000 images the model never saw during training or tuning. We measure accuracy, precision, recall, F1-score, and ROC-AUC on that set only — not on the training data.',
  },
]

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="section">
      <div className="container how">
        <span className="label">How it works</span>
        <ol className="how__list">
          {STEPS.map(step => (
            <li key={step.num} className="how__step">
              <span className="how__num" aria-hidden="true">{step.num}</span>
              <div>
                <h3 className="how__title">{step.title}</h3>
                <p  className="how__body" >{step.body}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
