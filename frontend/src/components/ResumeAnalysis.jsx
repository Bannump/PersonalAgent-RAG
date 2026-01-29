import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaUpload, FaSpinner, FaChartLine, FaKey, FaCheckCircle } from 'react-icons/fa'
import { useDropzone } from 'react-dropzone'
import { resumeAnalysis } from '../services/api'
import './ResumeAnalysis.css'

function ResumeAnalysis() {
  const navigate = useNavigate()
  const [resume, setResume] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const resultsRef = useRef(null)

  const onDropResume = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setResume(acceptedFiles[0])
      setError(null)
    }
  }

  const { getRootProps: getResumeRootProps, getInputProps: getResumeInputProps, isDragActive: isResumeDragActive } = useDropzone({
    onDrop: onDropResume,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt']
    },
    multiple: false
  })

  const handleAnalyze = async () => {
    if (!resume || !jobDescription.trim()) {
      setError('Please upload a resume and provide a job description')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeAnalysis.jsx:handleAnalyze',message:'Starting resume analysis',data:{hasResume:!!resume,resumeName:resume?.name,resumeSize:resume?.size,resumeType:resume?.type,jobDescLength:jobDescription.length},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      
      const formData = new FormData()
      formData.append('resume', resume)
      formData.append('job_description', jobDescription)

      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeAnalysis.jsx:handleAnalyze',message:'FormData constructed',data:{formDataKeys:Array.from(formData.keys()),hasResumeField:formData.has('resume'),hasJobDescField:formData.has('job_description')},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion
      
      const response = await resumeAnalysis(formData)
      
      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeAnalysis.jsx:handleAnalyze',message:'Resume analysis succeeded',data:{hasResponse:!!response,responseKeys:response?Object.keys(response):[]},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      
      setResult(response)
    } catch (err) {
      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'ResumeAnalysis.jsx:handleAnalyze',message:'Resume analysis failed',data:{errorType:err?.constructor?.name,errorMessage:err?.message,hasRequest:!!err?.request,hasResponse:!!err?.response,status:err?.response?.status,statusText:err?.response?.statusText,responseData:err?.response?.data},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
      // #endregion
      
      setError(err.response?.data?.error || err.message || 'Failed to analyze resume. Please try again.')
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

  const getScoreColor = (score) => {
    if (score >= 80) return '#10b981'
    if (score >= 60) return '#f59e0b'
    if (score >= 40) return '#f97316'
    return '#ef4444'
  }

  const getScoreLabel = (score) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    if (score >= 40) return 'Needs Improvement'
    return 'Poor'
  }

  return (
    <div className="resume-analysis">
      <header className="page-header">
        <button className="back-button" onClick={() => navigate('/')}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1>📄 Resume Analysis & ATS Optimization</h1>
      </header>

      <main className="page-main">
        <div className="container">
          <div className="upload-section">
            <div className="upload-group">
              <label>Upload Resume</label>
              <div
                {...getResumeRootProps()}
                className={`dropzone ${isResumeDragActive ? 'active' : ''} ${resume ? 'has-file' : ''}`}
                data-tutorial="resume-upload"
              >
                <input {...getResumeInputProps()} />
                {resume ? (
                  <div className="file-preview">
                    <FaCheckCircle className="check-icon" />
                    <p>{resume.name}</p>
                    <button
                      className="remove-file"
                      onClick={(e) => {
                        e.stopPropagation()
                        setResume(null)
                      }}
                    >
                      Remove
                    </button>
                  </div>
                ) : (
                  <div className="dropzone-content">
                    <FaUpload size={32} />
                    <p>{isResumeDragActive ? 'Drop resume here' : 'Drag & drop resume or click to select'}</p>
                    <p className="hint">Supports: PDF, DOCX, TXT</p>
                  </div>
                )}
              </div>
            </div>

            <div className="job-description-section" data-tutorial="resume-job-description">
              <label htmlFor="job-description">Job Description *</label>
              <textarea
                id="job-description"
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                rows={10}
              />
            </div>

            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={!resume || !jobDescription.trim() || loading}
              data-tutorial="resume-analyze"
            >
              {loading ? (
                <>
                  <FaSpinner className="spinner" /> Analyzing...
                </>
              ) : (
                <>
                  <FaChartLine /> Analyze Resume
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
            <div ref={resultsRef} className="result-section" data-tutorial="resume-results">
              <h2>📊 Analysis Results</h2>

              <div className="score-card" style={{ borderColor: getScoreColor(result.ats_score) }}>
                <div className="score-main">
                  <div className="score-circle" style={{ borderColor: getScoreColor(result.ats_score) }}>
                    <span style={{ color: getScoreColor(result.ats_score) }}>{result.ats_score}</span>
                    <small>/100</small>
                  </div>
                  <div className="score-info">
                    <h3>ATS Score</h3>
                    <p className="score-label" style={{ color: getScoreColor(result.ats_score) }}>
                      {getScoreLabel(result.ats_score)}
                    </p>
                  </div>
                </div>
              </div>

              <div className="results-grid">
                <div className="result-card">
                  <h3><FaKey /> Keyword Analysis</h3>
                  <div className="metric">
                    <span className="metric-label">Match Score:</span>
                    <span className="metric-value">{result.keyword_analysis?.match_score?.toFixed(1)}%</span>
                  </div>
                  {result.keyword_analysis?.missing_keywords && result.keyword_analysis.missing_keywords.length > 0 && (
                    <div className="keywords-list">
                      <p className="keywords-title">Top Missing Keywords:</p>
                      <div className="keywords-tags">
                        {result.keyword_analysis.missing_keywords.slice(0, 10).map((keyword, index) => (
                          <span key={index} className="keyword-tag missing">{keyword}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {result.keyword_analysis?.common_keywords && result.keyword_analysis.common_keywords.length > 0 && (
                    <div className="keywords-list">
                      <p className="keywords-title">Common Keywords:</p>
                      <div className="keywords-tags">
                        {result.keyword_analysis.common_keywords.slice(0, 10).map((keyword, index) => (
                          <span key={index} className="keyword-tag common">{keyword}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {result.skills_analysis && (
                  <div className="result-card">
                    <h3>💼 Skills Analysis</h3>
                    <div className="metric">
                      <span className="metric-label">Skill Match:</span>
                      <span className="metric-value">{result.skills_analysis.skill_match_percentage?.toFixed(1)}%</span>
                    </div>
                    {result.skills_analysis.missing_skills && result.skills_analysis.missing_skills.length > 0 && (
                      <div className="skills-list">
                        <p className="skills-title">Missing Skills:</p>
                        <ul>
                          {result.skills_analysis.missing_skills.slice(0, 10).map((skill, index) => (
                            <li key={index}>{skill}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {result.recommendations && result.recommendations.length > 0 && (
                <div className="result-card recommendations">
                  <h3>💡 Recommendations</h3>
                  <ul>
                    {result.recommendations.map((rec, index) => (
                      <li key={index}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default ResumeAnalysis
