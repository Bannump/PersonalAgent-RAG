import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { TutorialProvider } from './contexts/TutorialContext'
import Dashboard from './components/Dashboard'
import VehicleDiagnostics from './components/VehicleDiagnostics'
import ResumeAnalysis from './components/ResumeAnalysis'
import ResumeBuilder from './components/ResumeBuilder'
import ChatBot from './components/ChatBot'
import TutorialButton from './components/TutorialButton'
import TutorialOverlay from './components/TutorialOverlay'
import './App.css'

function App() {
  return (
    <TutorialProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/vehicle" element={<VehicleDiagnostics />} />
            <Route path="/resume-analysis" element={<ResumeAnalysis />} />
            <Route path="/resume-builder" element={<ResumeBuilder />} />
          </Routes>
          <TutorialButton />
          <ChatBot />
          <TutorialOverlay />
        </div>
      </Router>
    </TutorialProvider>
  )
}

export default App
