import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaGraduationCap, FaCar, FaFileAlt, FaBriefcase, FaTimes } from 'react-icons/fa'
import { useTutorial } from '../contexts/TutorialContext'
import './TutorialButton.css'

function TutorialButton() {
  const [showMenu, setShowMenu] = useState(false)
  const [showTooltip, setShowTooltip] = useState(false)
  const navigate = useNavigate()
  const { startTutorial } = useTutorial()

  const handleTutorialClick = (feature) => {
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'TutorialButton.jsx:handleTutorialClick',message:'Tutorial button clicked',data:{feature,currentPath:window.location.pathname},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
    // #endregion
    setShowMenu(false)
    navigate('/')
    setTimeout(() => startTutorial(feature), 500)
  }

  const tutorials = [
    {
      id: 'vehicle',
      name: 'Vehicle Diagnostics',
      icon: <FaCar />,
      description: 'Learn how to diagnose vehicle issues'
    },
    {
      id: 'resume-analysis',
      name: 'Resume Analysis',
      icon: <FaFileAlt />,
      description: 'Master resume optimization techniques'
    },
    {
      id: 'resume-builder',
      name: 'Resume Builder',
      icon: <FaBriefcase />,
      description: 'Build ATS-optimized resumes'
    }
  ]

  return (
    <>
      <div className="tutorial-button-wrapper">
        <button
          className="tutorial-button-main"
          onClick={() => setShowMenu(!showMenu)}
          onMouseEnter={() => setShowTooltip(true)}
          onMouseLeave={() => setShowTooltip(false)}
          aria-label="Interactive Tutorials"
        >
          <FaGraduationCap className="tutorial-icon" />
          <span className="tutorial-button-text">Tutorials</span>
        </button>

        {showTooltip && !showMenu && (
          <div className="tutorial-tooltip-bubble">
            <div className="tutorial-tooltip-arrow"></div>
            <p className="tutorial-tooltip-title">Interactive Tutorials</p>
            <p className="tutorial-tooltip-description">
              Step-by-step guides to master all features
            </p>
          </div>
        )}

        {showMenu && (
          <div className="tutorial-menu-dropdown">
            <div className="tutorial-menu-header">
              <h3>Interactive Tutorials</h3>
              <button
                className="tutorial-menu-close"
                onClick={() => setShowMenu(false)}
                aria-label="Close menu"
              >
                <FaTimes />
              </button>
            </div>
            <p className="tutorial-menu-subtitle">
              Choose a tutorial to get started
            </p>
            <div className="tutorial-menu-items">
              {tutorials.map((tutorial) => (
                <button
                  key={tutorial.id}
                  className="tutorial-menu-item"
                  onClick={() => handleTutorialClick(tutorial.id)}
                >
                  <div className="tutorial-menu-icon">{tutorial.icon}</div>
                  <div className="tutorial-menu-content">
                    <div className="tutorial-menu-name">{tutorial.name}</div>
                    <div className="tutorial-menu-desc">{tutorial.description}</div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
      {showMenu && (
        <div
          className="tutorial-menu-backdrop"
          onClick={() => setShowMenu(false)}
        />
      )}
    </>
  )
}

export default TutorialButton
