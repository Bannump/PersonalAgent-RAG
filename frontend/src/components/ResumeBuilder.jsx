import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaDownload, FaSpinner, FaPlus, FaTrash } from 'react-icons/fa'
import { resumeBuilder } from '../services/api'
import './ResumeBuilder.css'

function ResumeBuilder() {
  const navigate = useNavigate()
  const STORAGE_KEY = 'resume_builder_form_data'
  
  // Load form data from localStorage on mount
  const loadFormData = () => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      if (saved) {
        const parsed = JSON.parse(saved)
        return {
          experiences: parsed.experiences && parsed.experiences.length > 0 
            ? parsed.experiences 
            : [{ title: '', company: '', duration: '', description: '' }],
          skills: parsed.skills && parsed.skills.length > 0 
            ? parsed.skills 
            : [''],
          education: parsed.education && parsed.education.length > 0 
            ? parsed.education 
            : [{ degree: '', institution: '', year: '', details: '' }],
          portfolio: parsed.portfolio && parsed.portfolio.length > 0 
            ? parsed.portfolio 
            : [{ name: '', description: '' }],
          target_job: parsed.target_job || ''
        }
      }
    } catch (err) {
      console.error('Failed to load form data from localStorage:', err)
    }
    return {
      experiences: [{ title: '', company: '', duration: '', description: '' }],
      skills: [''],
      education: [{ degree: '', institution: '', year: '', details: '' }],
      portfolio: [{ name: '', description: '' }],
      target_job: ''
    }
  }
  
  const [formData, setFormData] = useState(loadFormData())
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const resultsRef = useRef(null)
  
  // Save form data to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(formData))
    } catch (err) {
      console.error('Failed to save form data to localStorage:', err)
    }
  }, [formData])

  const updateField = (section, index, field, value) => {
    const newData = { ...formData }
    newData[section][index][field] = value
    setFormData(newData)
  }

  const updateSkills = (index, value) => {
    const newSkills = [...formData.skills]
    newSkills[index] = value
    setFormData({ ...formData, skills: newSkills })
  }

  const addItem = (section) => {
    const defaults = {
      experiences: { title: '', company: '', duration: '', description: '' },
      education: { degree: '', institution: '', year: '', details: '' },
      portfolio: { name: '', description: '' }
    }
    setFormData({
      ...formData,
      [section]: [...formData[section], defaults[section]]
    })
  }

  const removeItem = (section, index) => {
    setFormData({
      ...formData,
      [section]: formData[section].filter((_, i) => i !== index)
    })
  }

  const addSkill = () => {
    setFormData({
      ...formData,
      skills: [...formData.skills, '']
    })
  }

  const removeSkill = (index) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter((_, i) => i !== index)
    })
  }

  const handleBuild = async () => {
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeBuilder.jsx:handleBuild',message:'Starting resume build',data:{experiencesCount:formData.experiences.length,skillsCount:formData.skills.length,educationCount:formData.education.length,portfolioCount:formData.portfolio.length,hasTargetJob:!!formData.target_job},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
    // #endregion
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const cleanData = {
        experiences: formData.experiences.filter(exp => exp.title && exp.company),
        skills: formData.skills.filter(skill => skill.trim()),
        education: formData.education.filter(edu => edu.degree && edu.institution),
        portfolio: formData.portfolio.filter(proj => proj.name),
        target_job: formData.target_job || undefined,
        output_format: 'pdf'  // Request PDF format (will fall back to .tex if pdflatex not available)
      }

      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeBuilder.jsx:handleBuild',message:'Clean data prepared',data:{cleanExperiencesCount:cleanData.experiences.length,cleanSkillsCount:cleanData.skills.length,cleanEducationCount:cleanData.education.length,cleanPortfolioCount:cleanData.portfolio.length,hasTargetJob:!!cleanData.target_job},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion

      const response = await resumeBuilder(cleanData)
      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeBuilder.jsx:handleBuild',message:'Resume build succeeded',data:{hasResponse:!!response,responseKeys:response?Object.keys(response):[]},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      setResult(response)
    } catch (err) {
      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeBuilder.jsx:handleBuild',message:'Resume build failed',data:{errorType:err?.constructor?.name,errorMessage:err?.message,hasRequest:!!err?.request,hasResponse:!!err?.response,status:err?.response?.status,responseData:err?.response?.data},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
      // #endregion
      setError(err.response?.data?.error || 'Failed to build resume. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  // Scroll to results when result is set
  useEffect(() => {
    if (result && resultsRef.current) {
      setTimeout(() => {
        const element = resultsRef.current
        if (element) {
          const elementTop = element.getBoundingClientRect().top + window.pageYOffset
          const offset = 100 // Offset to show beginning of results with some spacing
          window.scrollTo({ top: elementTop - offset, behavior: 'smooth' })
        }
      }, 100) // Small delay to ensure DOM is updated
    }
  }, [result])

  return (
    <div className="resume-builder">
      <header className="page-header">
        <button className="back-button" onClick={() => navigate('/')}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1>📝 Resume Builder</h1>
      </header>

      <main className="page-main">
        <div className="container">
          <div className="builder-form">
            <section className="form-section" data-tutorial="builder-experience">
              <h2>Work Experience</h2>
              {formData.experiences.map((exp, index) => (
                <div key={index} className="form-item">
                  <div className="form-row">
                    <input
                      type="text"
                      placeholder="Job Title"
                      value={exp.title}
                      onChange={(e) => updateField('experiences', index, 'title', e.target.value)}
                    />
                    <input
                      type="text"
                      placeholder="Company"
                      value={exp.company}
                      onChange={(e) => updateField('experiences', index, 'company', e.target.value)}
                    />
                    <input
                      type="text"
                      placeholder="Duration (e.g., 2020 - 2024)"
                      value={exp.duration}
                      onChange={(e) => updateField('experiences', index, 'duration', e.target.value)}
                    />
                    {formData.experiences.length > 1 && (
                      <button className="remove-button" onClick={() => removeItem('experiences', index)}>
                        <FaTrash />
                      </button>
                    )}
                  </div>
                  <textarea
                    placeholder="Job description and achievements..."
                    value={exp.description}
                    onChange={(e) => updateField('experiences', index, 'description', e.target.value)}
                    rows={3}
                  />
                </div>
              ))}
              <button className="add-button" onClick={() => addItem('experiences')}>
                <FaPlus /> Add Experience
              </button>
            </section>

            <section className="form-section" data-tutorial="builder-skills">
              <h2>Skills</h2>
              <div className="skills-input">
                {formData.skills.map((skill, index) => (
                  <div key={index} className="skill-input-row">
                    <input
                      type="text"
                      placeholder="Skill"
                      value={skill}
                      onChange={(e) => updateSkills(index, e.target.value)}
                    />
                    {formData.skills.length > 1 && (
                      <button className="remove-button" onClick={() => removeSkill(index)}>
                        <FaTrash />
                      </button>
                    )}
                  </div>
                ))}
                <button className="add-button" onClick={addSkill}>
                  <FaPlus /> Add Skill
                </button>
              </div>
            </section>

            <section className="form-section" data-tutorial="builder-education">
              <h2>Education</h2>
              {formData.education.map((edu, index) => (
                <div key={index} className="form-item">
                  <div className="form-row">
                    <input
                      type="text"
                      placeholder="Degree"
                      value={edu.degree}
                      onChange={(e) => updateField('education', index, 'degree', e.target.value)}
                    />
                    <input
                      type="text"
                      placeholder="Institution"
                      value={edu.institution}
                      onChange={(e) => updateField('education', index, 'institution', e.target.value)}
                    />
                    <input
                      type="text"
                      placeholder="Year"
                      value={edu.year}
                      onChange={(e) => updateField('education', index, 'year', e.target.value)}
                    />
                    {formData.education.length > 1 && (
                      <button className="remove-button" onClick={() => removeItem('education', index)}>
                        <FaTrash />
                      </button>
                    )}
                  </div>
                  <textarea
                    placeholder="Additional details (GPA, honors, coursework, etc.)"
                    value={edu.details}
                    onChange={(e) => updateField('education', index, 'details', e.target.value)}
                    rows={2}
                  />
                </div>
              ))}
              <button className="add-button" onClick={() => addItem('education')}>
                <FaPlus /> Add Education
              </button>
            </section>

            <section className="form-section">
              <h2>Portfolio/Projects (Optional)</h2>
              {formData.portfolio.map((proj, index) => (
                <div key={index} className="form-item">
                  <div className="form-row">
                    <input
                      type="text"
                      placeholder="Project Name"
                      value={proj.name}
                      onChange={(e) => updateField('portfolio', index, 'name', e.target.value)}
                      style={{ flex: 1 }}
                    />
                    {formData.portfolio.length > 1 && (
                      <button className="remove-button" onClick={() => removeItem('portfolio', index)}>
                        <FaTrash />
                      </button>
                    )}
                  </div>
                  <textarea
                    placeholder="Project description..."
                    value={proj.description}
                    onChange={(e) => updateField('portfolio', index, 'description', e.target.value)}
                    rows={2}
                  />
                </div>
              ))}
              <button className="add-button" onClick={() => addItem('portfolio')}>
                <FaPlus /> Add Project
              </button>
            </section>

            <section className="form-section" data-tutorial="builder-target-job">
              <h2>Target Job (Optional)</h2>
              <textarea
                placeholder="Describe the target job position for optimization..."
                value={formData.target_job}
                onChange={(e) => setFormData({ ...formData, target_job: e.target.value })}
                rows={4}
              />
            </section>

            <button
              className="build-button"
              onClick={handleBuild}
              disabled={loading}
              data-tutorial="builder-build"
            >
              {loading ? (
                <>
                  <FaSpinner className="spinner" /> Building Resume...
                </>
              ) : (
                <>
                  <FaDownload /> Build Resume
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {result && (
            <div ref={resultsRef} className="result-section" data-tutorial="builder-results">
              <h2>✅ Resume Built Successfully!</h2>
              <div className="result-card">
                <p><strong>File:</strong> {result.file_path}</p>
                <p><strong>Format:</strong> {result.format}</p>
                {result.download_url && (
                  <a
                    href={`${import.meta.env.VITE_API_URL || ''}${result.download_url}`}
                    download
                    className="download-button"
                  >
                    <FaDownload /> Download Resume
                  </a>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default ResumeBuilder
