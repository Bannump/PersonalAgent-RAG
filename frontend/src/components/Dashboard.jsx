import React from 'react'
import { useNavigate } from 'react-router-dom'
import { FaCar, FaFileAlt, FaUserEdit, FaRobot } from 'react-icons/fa'
import './Dashboard.css'

function Dashboard() {
  const navigate = useNavigate()

  const features = [
    {
      id: 'vehicle',
      title: 'Vehicle Diagnostics',
      description: 'Analyze car dashboard images and get instant solutions',
      icon: <FaCar size={48} />,
      path: '/vehicle',
      color: '#3b82f6'
    },
    {
      id: 'resume-analysis',
      title: 'Resume Analysis',
      description: 'Compare your resume against job descriptions with ATS optimization',
      icon: <FaFileAlt size={48} />,
      path: '/resume-analysis',
      color: '#10b981'
    },
    {
      id: 'resume-builder',
      title: 'Resume Builder',
      description: 'Build optimized resumes from your experiences and skills',
      icon: <FaUserEdit size={48} />,
      path: '/resume-builder',
      color: '#f59e0b'
    }
  ]

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo">
            <FaRobot size={32} />
            <h1>My Personal Agent</h1>
          </div>
          <p className="tagline">Your AI-powered personal assistant</p>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-container">
          <section className="hero-section">
            <h2 className="hero-title">Welcome to Your Personal Agent</h2>
            <p className="hero-description">
              A sophisticated RAG-powered assistant for vehicle diagnostics and resume optimization
            </p>
          </section>

          <section className="features-section">
            <h3 className="section-title">Available Features</h3>
            <div className="features-grid">
              {features.map((feature) => (
                <div
                  key={feature.id}
                  className="feature-card"
                  onClick={() => navigate(feature.path)}
                  style={{ '--accent-color': feature.color }}
                  data-tutorial={`dashboard-${feature.id}-card`}
                >
                  <div className="feature-icon" style={{ color: feature.color }}>
                    {feature.icon}
                  </div>
                  <h4 className="feature-title">{feature.title}</h4>
                  <p className="feature-description">{feature.description}</p>
                  <button className="feature-button" data-tutorial={`dashboard-${feature.id}-button`}>
                    Get Started →
                  </button>
                </div>
              ))}
            </div>
          </section>

          <section className="info-section">
            <div className="info-card">
              <h4>🚀 Powered by AI</h4>
              <p>Built with OpenAI GPT-4 and ChromaDB for intelligent assistance</p>
            </div>
            <div className="info-card">
              <h4>🔒 Secure & Private</h4>
              <p>Your data is processed securely with industry-standard encryption</p>
            </div>
            <div className="info-card">
              <h4>⚡ Fast & Efficient</h4>
              <p>Get instant results with optimized AI models and caching</p>
            </div>
          </section>
        </div>
      </main>

      <footer className="dashboard-footer">
        <p>&copy; 2024 My Personal Agent. Built with ❤️ using React & Python.</p>
      </footer>
    </div>
  )
}

export default Dashboard
