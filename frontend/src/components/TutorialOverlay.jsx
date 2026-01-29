import React, { useEffect, useRef } from 'react'
import { FaTimes, FaChevronLeft, FaChevronRight, FaCheck } from 'react-icons/fa'
import { useTutorial } from '../contexts/TutorialContext'
import './TutorialOverlay.css'

function TutorialOverlay() {
  const {
    isActive,
    currentStep,
    totalSteps,
    highlightedElement,
    nextStep,
    previousStep,
    endTutorial,
    skipTutorial
  } = useTutorial()

  const overlayRef = useRef(null)
  const spotlightRef = useRef(null)
  const tooltipRef = useRef(null)

  useEffect(() => {
    if (!isActive || !highlightedElement) {
      if (overlayRef.current) {
        overlayRef.current.style.display = 'none'
      }
      if (tooltipRef.current) {
        tooltipRef.current.classList.remove('transitioning')
      }
      return
    }

    const element = highlightedElement.element
    if (!element) return

    let scrollTimeoutId = null
    let isInitialPositioning = true

    const updateSpotlight = () => {
      const rect = element.getBoundingClientRect()
      const overlay = overlayRef.current
      const spotlight = spotlightRef.current
      const tooltip = tooltipRef.current

      if (!overlay || !spotlight || !tooltip) return

      overlay.style.display = 'block'

      // Calculate spotlight position and size - use actual element dimensions with small padding
      const padding = 8 // Reduced padding for tighter highlight
      const spotlightWidth = rect.width + (padding * 2)
      const spotlightHeight = rect.height + (padding * 2)
      const spotlightX = rect.left - padding
      const spotlightY = rect.top - padding

      // Set spotlight position - use actual element dimensions, not square
      spotlight.style.width = `${spotlightWidth}px`
      spotlight.style.height = `${spotlightHeight}px`
      spotlight.style.left = `${spotlightX}px`
      spotlight.style.top = `${spotlightY}px`
      spotlight.style.borderRadius = '8px'

      // Update tooltip position
      const position = highlightedElement.position || 'bottom'
      
      // Force reflow to get accurate tooltip dimensions
      // Temporarily hide transitions to get stable measurements
      const wasTransitioning = tooltip.classList.contains('transitioning')
      if (!wasTransitioning) {
        tooltip.style.transition = 'none'
      }
      
      // Get tooltip dimensions - force layout calculation
      const tooltipRect = tooltip.getBoundingClientRect()
      const tooltipHeight = tooltipRect.height || tooltip.offsetHeight || 150 // fallback
      const tooltipWidth = tooltipRect.width || tooltip.offsetWidth || 400 // fallback
      
      let tooltipTop = rect.bottom + 20
      let tooltipLeft = rect.left + rect.width / 2
      let tooltipTransform = 'translateX(-50%)'

      if (position === 'top') {
        tooltipTop = rect.top - tooltipHeight - 20
      } else if (position === 'left') {
        tooltipLeft = rect.left - tooltipWidth - 20
        tooltipTransform = 'translateY(-50%)'
        tooltipTop = rect.top + rect.height / 2
      } else if (position === 'right') {
        tooltipLeft = rect.right + 20
        tooltipTransform = 'translateY(-50%)'
        tooltipTop = rect.top + rect.height / 2
      }

      // Ensure tooltip is visible
      const viewportWidth = window.innerWidth
      const viewportHeight = window.innerHeight

      if (tooltipLeft < 20) {
        tooltipLeft = 20
        tooltipTransform = 'none'
      } else if (tooltipLeft + tooltipWidth > viewportWidth - 20) {
        tooltipLeft = viewportWidth - tooltipWidth - 20
        tooltipTransform = 'none'
      }

      if (tooltipTop < 20) {
        tooltipTop = 20
      } else if (tooltipTop + tooltipHeight > viewportHeight - 20) {
        tooltipTop = viewportHeight - tooltipHeight - 20
      }

      // Use requestAnimationFrame to ensure smooth transition
      requestAnimationFrame(() => {
        if (tooltip) {
          // Restore transition after setting position if it was disabled
          if (!wasTransitioning) {
            tooltip.style.transition = ''
          }
          tooltip.style.top = `${tooltipTop}px`
          tooltip.style.left = `${tooltipLeft}px`
          tooltip.style.transform = tooltipTransform
          // Remove transitioning class after positioning is stable
          if (!isInitialPositioning) {
            tooltip.classList.remove('transitioning')
          }
        }
      })

      // Add highlight class to element
      element.classList.add('tutorial-highlighted')
    }

    // Debounced scroll handler - only update after scroll stops
    const handleScroll = () => {
      // Clear existing timeout
      if (scrollTimeoutId) {
        clearTimeout(scrollTimeoutId)
      }
      // Only update during scroll if not initial positioning
      if (!isInitialPositioning) {
        scrollTimeoutId = setTimeout(() => {
          updateSpotlight()
        }, 150) // Wait for scroll to settle
      }
    }

    // Small delay to ensure DOM is ready before updating position
    // Add transitioning class briefly to smooth the transition
    const tooltip = tooltipRef.current
    if (tooltip) {
      tooltip.classList.add('transitioning')
    }

    // Wait longer for smooth scroll to complete before final positioning
    // Smooth scroll typically takes 300-500ms, so wait 700ms to ensure it's fully complete
    // This prevents tooltip from recalculating during scroll
    const initialTimeout = setTimeout(() => {
      // Update once more with accurate dimensions after scroll completes
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          // Double RAF to ensure layout is fully stable
          isInitialPositioning = false
          updateSpotlight()
          // Remove transitioning class after position is set
          if (tooltip) {
            setTimeout(() => {
              tooltip.classList.remove('transitioning')
            }, 150) // Slightly longer to ensure transition completes
          }
        })
      })
    }, 700)

    // Store timeout ID for cleanup
    scrollTimeoutId = initialTimeout

    const handleResize = () => updateSpotlight()

    window.addEventListener('resize', handleResize)
    window.addEventListener('scroll', handleScroll, true)

    return () => {
      window.removeEventListener('resize', handleResize)
      window.removeEventListener('scroll', handleScroll, true)
      if (scrollTimeoutId) {
        clearTimeout(scrollTimeoutId)
      }
      if (element) {
        element.classList.remove('tutorial-highlighted')
      }
      if (overlayRef.current) {
        overlayRef.current.style.display = 'none'
      }
      if (tooltipRef.current) {
        tooltipRef.current.classList.remove('transitioning')
      }
    }
  }, [isActive, highlightedElement])

  if (!isActive || !highlightedElement) {
    return null
  }

  const isFirstStep = currentStep === 0
  const isLastStep = currentStep === totalSteps - 1

  return (
    <div ref={overlayRef} className="tutorial-overlay">
      <div ref={spotlightRef} className="tutorial-spotlight"></div>
      <div ref={tooltipRef} className="tutorial-tooltip">
        <div className="tutorial-tooltip-header">
          <div className="tutorial-tooltip-title">
            {highlightedElement.title}
          </div>
          <button
            className="tutorial-close-button"
            onClick={skipTutorial}
            aria-label="Close tutorial"
          >
            <FaTimes />
          </button>
        </div>
        <div className="tutorial-tooltip-message">
          {highlightedElement.message}
        </div>
        <div className="tutorial-tooltip-footer">
          <div className="tutorial-progress">
            Step {currentStep + 1} of {totalSteps}
          </div>
          <div className="tutorial-navigation">
            {!isFirstStep && (
              <button
                className="tutorial-nav-button prev"
                onClick={previousStep}
                aria-label="Previous step"
              >
                <FaChevronLeft /> Previous
              </button>
            )}
            {isLastStep ? (
              <button
                className="tutorial-nav-button finish"
                onClick={endTutorial}
                aria-label="Finish tutorial"
              >
                <FaCheck /> Finish
              </button>
            ) : (
              <button
                className="tutorial-nav-button next"
                onClick={nextStep}
                aria-label="Next step"
              >
                Next <FaChevronRight />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default TutorialOverlay
