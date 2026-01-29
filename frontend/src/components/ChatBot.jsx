import React, { useState, useRef, useEffect } from 'react'
import { FaComments, FaTimes, FaPaperPlane, FaCar, FaFileAlt, FaBriefcase, FaQuestionCircle, FaRobot, FaGraduationCap } from 'react-icons/fa'
import { useNavigate } from 'react-router-dom'
import { useTutorial } from '../contexts/TutorialContext'
import './ChatBot.css'

function ChatBot() {
  const [isOpen, setIsOpen] = useState(false)
  const [showTutorialMenu, setShowTutorialMenu] = useState(false)
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hi! I'm your Personal Agent assistant. How can I help you today?",
      type: 'text'
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const navigate = useNavigate()
  const { startTutorial } = useTutorial()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const addMessage = (role, content, type = 'text') => {
    setMessages(prev => [...prev, { role, content, type, timestamp: new Date() }])
  }

  const handleQuickAction = (action) => {
    const actionMessages = {
      vehicle: {
        content: "🚗 **Vehicle Diagnostics** helps you diagnose car issues from dashboard images. Simply upload an image of your car's dashboard or any vehicle issue, and I'll analyze it to provide:\n\n• Diagnosis of the problem\n• Recommended actions\n• Emergency contacts if needed\n• Step-by-step solutions\n\nWould you like me to take you to the Vehicle Diagnostics page?",
        actions: ['Take me there', 'More info']
      },
      resume_analysis: {
        content: "📝 **Resume Analysis & ATS Optimization** helps you optimize your resume for job applications. Upload your resume and a job description, and I'll provide:\n\n• ATS compatibility score\n• Keyword matching analysis\n• Skills gap analysis\n• Detailed recommendations\n• Missing keywords from the job description\n\nWould you like me to take you to the Resume Analysis page?",
        actions: ['Take me there', 'More info']
      },
      resume_builder: {
        content: "💼 **Resume Builder** helps you create an ATS-optimized resume from scratch. Provide your:\n\n• Work experience\n• Skills\n• Education\n• Portfolio/projects\n• Target job description (optional)\n\nAnd I'll generate a professional resume that's optimized for ATS systems.\n\nWould you like me to take you to the Resume Builder page?",
        actions: ['Take me there', 'More info']
      }
    }

    const message = actionMessages[action]
    if (message) {
      addMessage('assistant', message.content, 'action')
      
      // Add action buttons
      setTimeout(() => {
        const lastMessage = { ...message, action, role: 'assistant', type: 'action' }
        setMessages(prev => {
          const newMessages = [...prev]
          newMessages[newMessages.length - 1] = lastMessage
          return newMessages
        })
      }, 0)
    }
  }

  const handleActionButton = (action, buttonText) => {
    if (buttonText === 'Take me there') {
      const routes = {
        vehicle: '/vehicle',
        resume_analysis: '/resume-analysis',
        resume_builder: '/resume-builder'
      }
      setIsOpen(false)
      navigate(routes[action])
    } else if (buttonText === 'More info') {
      // Add more detailed information
      const detailedInfo = {
        vehicle: `**How to use Vehicle Diagnostics:**

1. Click on the Vehicle Diagnostics feature in the dashboard
2. Upload an image of your car's dashboard, warning lights, or any vehicle issue
3. Optionally add a description of what happened
4. Click "Analyze Vehicle"
5. Get instant diagnosis and recommendations

**Tips:**
• Take clear, well-lit photos
• Include warning lights or error messages if visible
• Describe any sounds, smells, or behaviors

Would you like me to take you there now?`,
        resume_analysis: `**How to use Resume Analysis:**

1. Click on the Resume Analysis feature in the dashboard
2. Upload your resume (PDF, DOCX, or TXT)
3. Paste the job description you're applying for
4. Click "Analyze Resume"
5. Review your ATS score and recommendations

**Tips:**
• Use a recent, up-to-date resume
• Include the full job description for best results
• Review missing keywords and skills
• Update your resume based on recommendations

Would you like me to take you there now?`,
        resume_builder: `**How to use Resume Builder:**

1. Click on the Resume Builder feature in the dashboard
2. Fill in your work experience (title, company, duration, description)
3. Add your skills
4. Enter your education details
5. Optionally add portfolio projects
6. (Optional) Add a target job description for optimization
7. Click "Build Resume"
8. Download your ATS-optimized resume

**Tips:**
• Be specific with your job descriptions
• Highlight quantifiable achievements
• Include relevant keywords from your target job
• Review and customize the generated resume

Would you like me to take you there now?`
      }
      addMessage('assistant', detailedInfo[action])
    }
  }

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput('')
    addMessage('user', userMessage)
    setIsLoading(true)

    // Check for quick commands
    const lowerInput = userMessage.toLowerCase()
    
    if (lowerInput.includes('vehicle') || lowerInput.includes('car') || lowerInput.includes('diagnostic')) {
      handleQuickAction('vehicle')
      setIsLoading(false)
      return
    }
    
    if (lowerInput.includes('resume analysis') || lowerInput.includes('analyze resume') || lowerInput.includes('ats')) {
      handleQuickAction('resume_analysis')
      setIsLoading(false)
      return
    }
    
    if (lowerInput.includes('resume builder') || lowerInput.includes('build resume') || lowerInput.includes('create resume')) {
      handleQuickAction('resume_builder')
      setIsLoading(false)
      return
    }

    if (lowerInput.includes('help') || lowerInput.includes('what can you do')) {
      addMessage('assistant', `I can help you with several features:

🚗 **Vehicle Diagnostics** - Diagnose car issues from images
📝 **Resume Analysis** - Optimize your resume for job applications
💼 **Resume Builder** - Create ATS-optimized resumes

You can:
• Ask me questions about these features
• Request to be taken to any feature
• Get detailed instructions on how to use them
• View interactive tutorials for each feature
• Ask general questions and I'll do my best to help

Just type your question or use the quick action buttons below!`, 'feature_menu')
      setIsLoading(false)
      return
    }

    if (lowerInput.includes('tutorial') || lowerInput.includes('demo') || lowerInput.includes('how to use')) {
      setShowTutorialMenu(true)
      addMessage('assistant', `📚 **Interactive Tutorials Available!**

I can guide you through step-by-step demos for each feature with interactive highlights:

🚗 **Vehicle Diagnostics Tutorial** - Learn how to analyze vehicle issues
📝 **Resume Analysis Tutorial** - Master resume optimization
💼 **Resume Builder Tutorial** - Build your perfect resume

Click on "View Tutorials" button below or select a tutorial from the menu!`, 'tutorial_menu')
      setIsLoading(false)
      return
    }

    // TODO: Integrate with backend chat API when available
    // For now, provide helpful responses
    setTimeout(() => {
      let response = "I'm here to help! I can assist you with:\n\n"
      response += "• Vehicle diagnostics from images\n"
      response += "• Resume analysis and ATS optimization\n"
      response += "• Building ATS-optimized resumes\n\n"
      response += "You can ask me questions about these features, or use the quick action buttons below to explore them.\n\n"
      response += "Type 'help' to see all available options, or mention a feature name to get more information!"

      addMessage('assistant', response, 'feature_menu')
      setIsLoading(false)
    }, 1000)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <>
      <button
        className={`chatbot-toggle ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label="Toggle chatbot"
      >
        {isOpen ? <FaTimes /> : <FaComments />}
      </button>

      {isOpen && (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <div className="chatbot-header-content">
              <FaRobot className="chatbot-icon" />
              <div>
                <h3>Personal Agent</h3>
                <span className="chatbot-status">Online</span>
              </div>
            </div>
            <button
              className="chatbot-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chatbot"
            >
              <FaTimes />
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((message, index) => (
              <div key={index} className={`message ${message.role}`}>
                <div className="message-content">
                  {message.type === 'text' || message.type === 'action' ? (
                    <>
                      <div className="message-text" dangerouslySetInnerHTML={{ 
                        __html: message.content.replace(/\n/g, '<br/>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') 
                      }} />
                      {message.type === 'action' && message.actions && (
                        <div className="message-actions">
                          {message.actions.map((action, i) => (
                            <button
                              key={i}
                              className="action-button"
                              onClick={() => handleActionButton(message.action, action)}
                            >
                              {action}
                            </button>
                          ))}
                        </div>
                      )}
                    </>
                  ) : message.type === 'feature_menu' ? (
                    <>
                      <div className="message-text" dangerouslySetInnerHTML={{ 
                        __html: message.content.replace(/\n/g, '<br/>') 
                      }} />
                      <div className="quick-actions">
                        <button
                          className="quick-action-button"
                          onClick={() => handleQuickAction('vehicle')}
                        >
                          <FaCar /> Vehicle Diagnostics
                        </button>
                        <button
                          className="quick-action-button"
                          onClick={() => handleQuickAction('resume_analysis')}
                        >
                          <FaFileAlt /> Resume Analysis
                        </button>
                        <button
                          className="quick-action-button"
                          onClick={() => handleQuickAction('resume_builder')}
                        >
                          <FaBriefcase /> Resume Builder
                        </button>
                      </div>
                    </>
                  ) : message.type === 'tutorial_menu' ? (
                    <>
                      <div className="message-text" dangerouslySetInnerHTML={{ 
                        __html: message.content.replace(/\n/g, '<br/>') 
                      }} />
                      <div className="quick-actions">
                        <button
                          className="quick-action-button"
                          onClick={() => {
                            setIsOpen(false)
                            navigate('/')
                            setTimeout(() => startTutorial('vehicle'), 500)
                          }}
                        >
                          <FaCar /> Start Vehicle Tutorial
                        </button>
                        <button
                          className="quick-action-button"
                          onClick={() => {
                            setIsOpen(false)
                            navigate('/')
                            setTimeout(() => startTutorial('resume-analysis'), 500)
                          }}
                        >
                          <FaFileAlt /> Start Resume Analysis Tutorial
                        </button>
                        <button
                          className="quick-action-button"
                          onClick={() => {
                            setIsOpen(false)
                            navigate('/')
                            setTimeout(() => startTutorial('resume-builder'), 500)
                          }}
                        >
                          <FaBriefcase /> Start Resume Builder Tutorial
                        </button>
                      </div>
                    </>
                  ) : null}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message assistant">
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input-container">
            <div className="quick-actions-horizontal">
              <button
                className="quick-action-icon"
                onClick={() => handleQuickAction('vehicle')}
                title="Vehicle Diagnostics"
              >
                <FaCar />
              </button>
              <button
                className="quick-action-icon"
                onClick={() => handleQuickAction('resume_analysis')}
                title="Resume Analysis"
              >
                <FaFileAlt />
              </button>
              <button
                className="quick-action-icon"
                onClick={() => handleQuickAction('resume_builder')}
                title="Resume Builder"
              >
                <FaBriefcase />
              </button>
              <button
                className="quick-action-icon tutorial-button"
                onClick={() => {
                  setShowTutorialMenu(!showTutorialMenu)
                  if (!showTutorialMenu) {
                    addMessage('user', 'tutorial')
                    handleSend()
                  }
                }}
                title="View Tutorials"
              >
                <FaGraduationCap />
              </button>
              <button
                className="quick-action-icon"
                onClick={() => {
                  addMessage('user', 'help')
                  handleSend()
                }}
                title="Help"
              >
                <FaQuestionCircle />
              </button>
            </div>
            {showTutorialMenu && (
              <div className="tutorial-menu">
                <div className="tutorial-menu-header">📚 Interactive Tutorials</div>
                <button
                  className="tutorial-menu-item"
                  onClick={() => {
                    setShowTutorialMenu(false)
                    setIsOpen(false)
                    navigate('/')
                    setTimeout(() => startTutorial('vehicle'), 500)
                  }}
                >
                  <FaCar /> Vehicle Diagnostics Tutorial
                </button>
                <button
                  className="tutorial-menu-item"
                  onClick={() => {
                    setShowTutorialMenu(false)
                    setIsOpen(false)
                    navigate('/')
                    setTimeout(() => startTutorial('resume-analysis'), 500)
                  }}
                >
                  <FaFileAlt /> Resume Analysis Tutorial
                </button>
                <button
                  className="tutorial-menu-item"
                  onClick={() => {
                    setShowTutorialMenu(false)
                    setIsOpen(false)
                    navigate('/')
                    setTimeout(() => startTutorial('resume-builder'), 500)
                  }}
                >
                  <FaBriefcase /> Resume Builder Tutorial
                </button>
              </div>
            )}
            <div className="input-wrapper">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                className="chatbot-input"
                disabled={isLoading}
              />
              <button
                className="send-button"
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
              >
                <FaPaperPlane />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default ChatBot
