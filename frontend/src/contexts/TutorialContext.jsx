import React, { createContext, useContext, useState, useCallback, useEffect } from 'react'

const TutorialContext = createContext()

export const useTutorial = () => {
  const context = useContext(TutorialContext)
  if (!context) {
    throw new Error('useTutorial must be used within TutorialProvider')
  }
  return context
}

export const TutorialProvider = ({ children }) => {
  const [isActive, setIsActive] = useState(false)
  const [currentFeature, setCurrentFeature] = useState(null)
  const [currentStep, setCurrentStep] = useState(0)
  const [highlightedElement, setHighlightedElement] = useState(null)
  const [tutorialSteps, setTutorialSteps] = useState([])

  // Tutorial step definitions
  const vehicleSteps = [
    {
      id: 'dashboard-vehicle-card',
      selector: '[data-tutorial="dashboard-vehicle-card"]',
      title: 'Step 1: Get Started',
      message: 'Click on "Get Started" button in the Vehicle Diagnostics card to begin.',
      position: 'bottom',
      action: 'highlight'
    },
    {
      id: 'vehicle-upload',
      selector: '[data-tutorial="vehicle-upload"]',
      title: 'Step 2: Upload Image',
      message: 'Drag & drop an image of your vehicle dashboard here, or click to select a file.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'upload'
    },
    {
      id: 'vehicle-description',
      selector: '[data-tutorial="vehicle-description"]',
      title: 'Step 3: Add Description (Recommended)',
      message: 'Although optional, adding a description of the issue helps provide better results. Describe what happened or what you notice.',
      position: 'top',
      action: 'highlight'
    },
    {
      id: 'vehicle-analyze',
      selector: '[data-tutorial="vehicle-analyze"]',
      title: 'Step 4: Analyze Vehicle',
      message: 'Click the "Analyze Vehicle" button to get instant diagnosis and recommendations.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'analyze'
    },
    {
      id: 'vehicle-results',
      selector: '[data-tutorial="vehicle-results"]',
      title: 'Step 5: View Results',
      message: 'Scroll down to check your analysis results. The results section will be highlighted.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'results'
    }
  ]

  const resumeAnalysisSteps = [
    {
      id: 'dashboard-resume-analysis-card',
      selector: '[data-tutorial="dashboard-resume-analysis-card"]',
      title: 'Step 1: Get Started',
      message: 'Click on "Get Started" button in the Resume Analysis card to begin.',
      position: 'bottom',
      action: 'highlight'
    },
    {
      id: 'resume-upload',
      selector: '[data-tutorial="resume-upload"]',
      title: 'Step 2: Upload Resume',
      message: 'Drag & drop your resume here (PDF, DOCX, or TXT), or click to select a file.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'upload'
    },
    {
      id: 'resume-job-description',
      selector: '[data-tutorial="resume-job-description"]',
      title: 'Step 3: Paste Job Description',
      message: 'Paste the job description you want to compare your resume against. This is required for analysis.',
      position: 'top',
      action: 'highlight'
    },
    {
      id: 'resume-analyze',
      selector: '[data-tutorial="resume-analyze"]',
      title: 'Step 4: Analyze Resume',
      message: 'Click the "Analyze Resume" button to get your ATS score and optimization recommendations.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'analyze'
    },
    {
      id: 'resume-results',
      selector: '[data-tutorial="resume-results"]',
      title: 'Step 5: Review Results',
      message: 'Scroll down to view your ATS score, keyword analysis, skills match, and recommendations.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'results'
    }
  ]

  const resumeBuilderSteps = [
    {
      id: 'dashboard-resume-builder-card',
      selector: '[data-tutorial="dashboard-resume-builder-card"]',
      title: 'Step 1: Get Started',
      message: 'Click on "Get Started" button in the Resume Builder card to begin.',
      position: 'bottom',
      action: 'highlight'
    },
    {
      id: 'builder-experience',
      selector: '[data-tutorial="builder-experience"]',
      title: 'Step 2: Add Work Experience',
      message: 'Fill in your work experience: job title, company, duration, and description. Click "Add Experience" to add more entries.',
      position: 'top',
      action: 'highlight'
    },
    {
      id: 'builder-skills',
      selector: '[data-tutorial="builder-skills"]',
      title: 'Step 3: Add Skills',
      message: 'List your skills. Click "Add Skill" to add more skills.',
      position: 'top',
      action: 'highlight'
    },
    {
      id: 'builder-education',
      selector: '[data-tutorial="builder-education"]',
      title: 'Step 4: Add Education',
      message: 'Enter your education details: degree, institution, year, and additional details.',
      position: 'top',
      action: 'highlight'
    },
    {
      id: 'builder-target-job',
      selector: '[data-tutorial="builder-target-job"]',
      title: 'Step 5: Target Job (Optional)',
      message: 'Optionally add a target job description to optimize your resume for a specific position.',
      position: 'top',
      action: 'highlight'
    },
    {
      id: 'builder-build',
      selector: '[data-tutorial="builder-build"]',
      title: 'Step 6: Build Resume',
      message: 'Click "Build Resume" to generate your ATS-optimized resume.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'build'
    },
    {
      id: 'builder-results',
      selector: '[data-tutorial="builder-results"]',
      title: 'Step 7: Download Resume',
      message: 'Once built, you can download your resume in the preferred format.',
      position: 'top',
      action: 'highlight',
      waitForAction: 'results'
    }
  ]

  const highlightStep = useCallback((step) => {
    if (!step) return

    const element = document.querySelector(step.selector)
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'TutorialContext.jsx:highlightStep',message:'Highlighting step',data:{stepId:step?.id,selector:step?.selector,elementFound:!!element,currentPath:window.location.pathname},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
    // #endregion
    if (element) {
      setHighlightedElement({
        element,
        title: step.title,
        message: step.message,
        position: step.position || 'bottom',
        stepId: step.id
      })
      
      // Scroll element into view
      element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    } else {
      // Element not found, try again after a short delay
      setTimeout(() => highlightStep(step), 200)
    }
  }, [])

  const startTutorial = useCallback((feature) => {
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'TutorialContext.jsx:startTutorial',message:'Tutorial started',data:{feature,currentPath:window.location.pathname},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
    // #endregion
    let steps = []
    
    switch (feature) {
      case 'vehicle':
        steps = vehicleSteps
        break
      case 'resume-analysis':
        steps = resumeAnalysisSteps
        break
      case 'resume-builder':
        steps = resumeBuilderSteps
        break
      default:
        // #region agent log
        fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'TutorialContext.jsx:startTutorial',message:'Invalid feature in tutorial',data:{feature},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
        // #endregion
        return
    }

    setTutorialSteps(steps)
    setCurrentFeature(feature)
    setCurrentStep(0)
    setIsActive(true)
    
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'TutorialContext.jsx:startTutorial',message:'Tutorial state set',data:{feature,stepsCount:steps.length,firstStepSelector:steps[0]?.selector},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'C'})}).catch(()=>{});
    // #endregion
    
    // Small delay to ensure DOM is ready after navigation
    setTimeout(() => {
      highlightStep(steps[0])
    }, 500)
  }, [highlightStep])

  const nextStep = useCallback(() => {
    if (currentStep < tutorialSteps.length - 1) {
      const next = currentStep + 1
      setCurrentStep(next)
      highlightStep(tutorialSteps[next])
    } else {
      endTutorial()
    }
  }, [currentStep, tutorialSteps, highlightStep])

  const previousStep = useCallback(() => {
    if (currentStep > 0) {
      const prev = currentStep - 1
      setCurrentStep(prev)
      highlightStep(tutorialSteps[prev])
    }
  }, [currentStep, tutorialSteps, highlightStep])

  const endTutorial = useCallback(() => {
    setIsActive(false)
    setCurrentFeature(null)
    setCurrentStep(0)
    setHighlightedElement(null)
    setTutorialSteps([])
  }, [])

  const skipTutorial = useCallback(() => {
    endTutorial()
  }, [endTutorial])

  // Auto-advance when navigating from dashboard step
  useEffect(() => {
    if (!isActive || currentStep !== 0) return

    const currentStepData = tutorialSteps[currentStep]
    if (!currentStepData || !currentStepData.id?.includes('dashboard')) return

    const checkNavigation = () => {
      const path = window.location.pathname
      const isOnFeaturePage = path === '/vehicle' || path === '/resume-analysis' || path === '/resume-builder'
      
      if (isOnFeaturePage && currentStep === 0) {
        // User navigated to feature page, move to step 2
        setTimeout(() => {
          if (currentStep === 0 && tutorialSteps.length > 1) {
            setCurrentStep(1)
            highlightStep(tutorialSteps[1])
          }
        }, 500)
      }
    }

    const interval = setInterval(checkNavigation, 300)
    return () => clearInterval(interval)
  }, [isActive, currentStep, tutorialSteps, highlightStep])

  // Auto-advance when actions are detected
  useEffect(() => {
    if (!isActive || !highlightedElement) return

    const currentStepData = tutorialSteps[currentStep]
    if (!currentStepData || !currentStepData.waitForAction) return

    const checkForAction = () => {
      if (currentStepData.waitForAction === 'upload') {
        // Check if file is uploaded
        const uploadElement = document.querySelector(currentStepData.selector)
        if (uploadElement) {
          const hasFile = uploadElement.classList.contains('has-image') || 
                         uploadElement.classList.contains('has-file') ||
                         uploadElement.querySelector('img') ||
                         uploadElement.querySelector('.check-icon')
          if (hasFile) {
            setTimeout(() => nextStep(), 1500)
          }
        }
      } else if (currentStepData.waitForAction === 'analyze' || 
                 currentStepData.waitForAction === 'build') {
        // Check if button is clicked - this will be handled by component
        // We'll listen for custom events
      } else if (currentStepData.waitForAction === 'results') {
        // Check if results are shown
        const resultsElement = document.querySelector(currentStepData.selector)
        if (resultsElement && resultsElement.offsetParent !== null) {
          setTimeout(() => {
            // Keep highlighting results - don't auto-advance, let user finish
          }, 1500)
        }
      }
    }

    const interval = setInterval(checkForAction, 500)
    return () => clearInterval(interval)
  }, [isActive, currentStep, tutorialSteps, highlightedElement, nextStep])

  const value = {
    isActive,
    currentFeature,
    currentStep,
    totalSteps: tutorialSteps.length,
    highlightedElement,
    startTutorial,
    nextStep,
    previousStep,
    endTutorial,
    skipTutorial
  }

  return (
    <TutorialContext.Provider value={value}>
      {children}
    </TutorialContext.Provider>
  )
}
