import React from 'react'
import Nav          from './components/Nav.jsx'
import Hero         from './components/Hero.jsx'
import Detector     from './components/Detector.jsx'
import HowItWorks   from './components/HowItWorks.jsx'
import ResultsTable from './components/ResultsTable.jsx'
import Limits       from './components/Limits.jsx'
import Footer       from './components/Footer.jsx'

export default function App() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Detector />
        <HowItWorks />
        <ResultsTable />
        <Limits />
      </main>
      <Footer />
    </>
  )
}
