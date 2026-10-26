import pathlib
ROOT = pathlib.Path(r"E:\3D")
C = ROOT / "app/frontend/src/components"
def w(name, content):
    (C / name).write_text(content, encoding="utf-8")
    print("  wrote", name)

# HowItWorks.jsx
w("HowItWorks.jsx", """\
import React from 'react'
import './HowItWorks.css'

const STEPS = [
  {
    num:   '01',
    title: 'Starting from ImageNet',
    body:  'We take ResNet-50, pretrained on ImageNet\u2019s 1.2 million photographs, as our backbone. Its early layers already detect edges, textures, and colour patterns \u2014 all useful for spotting the statistical fingerprints that GANs leave behind.',
  },
  {
    num:   '02',
    title: 'Two-stage fine-tuning',
    body:  'In the first stage we freeze the backbone and train only the final binary classifier \u2014 real or generated \u2014 for a few epochs. In the second stage we unfreeze the last residual block and fine-tune at a lower learning rate, letting the network adjust its highest-level features to this specific task.',
  },
  {
    num:   '03',
    title: 'Evaluation on held-out data',
    body:  'Before reporting any numbers we set aside 20,000 images the model never saw during training or tuning. We measure accuracy, precision, recall, F1-score, and ROC-AUC on that set only \u2014 not on the training data.',
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
""")

# HowItWorks.css
w("HowItWorks.css", """\
.how > .label { display: block; margin-bottom: 2.5rem; }

.how__list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 2.75rem;
}

.how__step {
  display: grid;
  grid-template-columns: 2.75rem 1fr;
  gap: 1.5rem;
  align-items: start;
}

.how__num {
  font-family: var(--font-serif);
  font-style: italic;
  font-size: 1.35rem;
  color: var(--text-secondary);
  padding-top: 0.1em;
}

.how__title {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  font-weight: 400;
  color: var(--text);
  margin-bottom: 0.5rem;
}

.how__body {
  max-width: 58ch;
  color: var(--text-secondary);
  font-size: 16px;
}

@media (max-width: 480px) {
  .how__step { grid-template-columns: 2rem 1fr; gap: 1rem; }
}
""")

# ResultsTable.jsx
w("ResultsTable.jsx", """\
import React from 'react'
import './ResultsTable.css'

const METRICS = [
  { name: 'Accuracy',  value: '98.88%' },
  { name: 'Precision', value: '98.56%' },
  { name: 'Recall',    value: '99.20%' },
  { name: 'F1-score',  value: '98.88%' },
  { name: 'ROC-AUC',   value: '0.9994' },
]

export default function ResultsTable() {
  return (
    <section id="results" className="section">
      <div className="container res">
        <span className="label">Results</span>
        <table className="res__table">
          <caption className="res__caption">
            Held-out test set, 20,000 images. Fake = positive class.
          </caption>
          <thead>
            <tr>
              <th scope="col">Metric</th>
              <th scope="col">Score</th>
            </tr>
          </thead>
          <tbody>
            {METRICS.map(m => (
              <tr key={m.name}>
                <td>{m.name}</td>
                <td>{m.value}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
""")

# ResultsTable.css
w("ResultsTable.css", """\
.res > .label { display: block; margin-bottom: 2rem; }

.res__table {
  width: 100%;
  max-width: 440px;
  border-collapse: collapse;
  font-size: 16px;
}

.res__caption {
  caption-side: bottom;
  font-size: 13px;
  color: var(--text-secondary);
  text-align: left;
  padding-top: 0.85rem;
}

.res__table th {
  text-align: left;
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-secondary);
  font-weight: 500;
  padding: 0 0 0.75rem;
  border-bottom: 1px solid var(--hairline);
}

.res__table th:last-child { text-align: right; }

.res__table td {
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--hairline);
  color: var(--text);
}

.res__table td:last-child {
  text-align: right;
  font-feature-settings: "tnum";
}

.res__table tr:last-child td { border-bottom: none; }
""")

# Limits.jsx
w("Limits.jsx", """\
import React from 'react'
import './Limits.css'

export default function Limits() {
  return (
    <section id="limits" className="section">
      <div className="container limits">
        <span className="label">Limits</span>
        <div className="limits__body">
          <p>
            This model was trained on one dataset: the{' '}
            <em>140k Real and Fake Faces</em> collection, which contains 256\u00d7256 pixel
            portraits generated by StyleGAN2. The training set is narrow by design \u2014
            we wanted clean numbers on a controlled problem before expanding scope.
          </p>
          <p>
            As a result, the model may not recognize images from other generators.
            A Midjourney portrait, a DALL\u00b7E face, or a Stable Diffusion rendering might
            return a low AI-probability even if it is clearly synthetic. Cross-generator
            evaluation is in progress and we will publish updated numbers when it is ready.
          </p>
          <p>
            The probabilities themselves can be overconfident. Because the model was trained
            on two very distinct populations \u2014 real FFHQ photographs and clean StyleGAN
            outputs \u2014 it tends to push predictions toward 0\u202f% or 100\u202f% rather than the middle.
            A score of 97\u202f% AI means <em>very likely generated by a GAN similar to
            StyleGAN</em>, not <em>97\u202f% certain this image is fake by any measure.</em>
          </p>
        </div>
      </div>
    </section>
  )
}
""")

# Limits.css
w("Limits.css", """\
.limits > .label { display: block; margin-bottom: 2rem; }

.limits__body {
  max-width: 58ch;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  color: var(--text-secondary);
}

.limits__body em {
  font-style: italic;
  color: var(--text);
}
""")

# Footer.jsx
w("Footer.jsx", """\
import React from 'react'
import './Footer.css'

export default function Footer() {
  return (
    <footer className="footer">
      <div className="container footer__inner">
        <p className="footer__names">
          [Your Name]\u2002\u00b7\u2002[Team Member]\u2002\u00b7\u2002[Team Member]
          <span className="footer__sep">\u2014</span>
          [Your College Name]
        </p>
        <p className="footer__note">
          Final-year project, 2024\u201325. Model weights are not distributed.
        </p>
      </div>
    </footer>
  )
}
""")

# Footer.css
w("Footer.css", """\
.footer {
  border-top: 1px solid var(--hairline);
  padding: 3rem 0 4rem;
}

.footer__inner {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.footer__names {
  font-size: 15px;
  color: var(--text);
}

.footer__sep {
  margin: 0 0.5rem;
  color: var(--text-secondary);
}

.footer__note {
  font-size: 13px;
  color: var(--text-secondary);
}
""")

print("All remaining components done.")
