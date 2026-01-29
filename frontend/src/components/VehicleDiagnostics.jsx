import React, { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { FaArrowLeft, FaUpload, FaSpinner, FaCheckCircle, FaPhone, FaExclamationTriangle } from 'react-icons/fa'
import { useDropzone } from 'react-dropzone'
import { vehicleDiagnostics } from '../services/api'
import './VehicleDiagnostics.css'

function VehicleDiagnostics() {
  const navigate = useNavigate()
  const [image, setImage] = useState(null)
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const resultsRef = useRef(null)

  const onDrop = (acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      setImage(acceptedFiles[0])
      setError(null)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    multiple: false
  })

  const handleAnalyze = async () => {
    if (!image) {
      setError('Please upload an image first')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'VehicleDiagnostics.jsx:handleAnalyze',message:'Starting vehicle diagnostics',data:{hasImage:!!image,imageName:image?.name,imageSize:image?.size,imageType:image?.type,hasDescription:!!description,descriptionLength:description?.length},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
    // #endregion

    try {
      const formData = new FormData()
      formData.append('image', image)
      formData.append('description', description)

      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'VehicleDiagnostics.jsx:handleAnalyze',message:'FormData constructed',data:{formDataKeys:Array.from(formData.keys()),hasImageField:formData.has('image'),hasDescriptionField:formData.has('description')},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
      // #endregion

      const response = await vehicleDiagnostics(formData)
      
      // #region agent log
      fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'VehicleDiagnostics.jsx:handleAnalyze',message:'Vehicle diagnostics succeeded',data:{hasResponse:!!response,responseKeys:response?Object.keys(response):[]},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
      // #endregion
      
      setResult(response)
    } catch (err) {
      console.error('Vehicle diagnostics error:', err)
      
      // Extract error message from different possible error formats
      let errorMessage = 'Failed to analyze image. Please try again.'
      
      if (err.response) {
        // Server responded with error
        const errorData = err.response.data
        if (errorData?.detail) {
          errorMessage = errorData.detail
        } else if (errorData?.error) {
          errorMessage = errorData.error
        } else if (typeof errorData === 'string') {
          errorMessage = errorData
        } else {
          errorMessage = `Server error: ${err.response.status} - ${err.response.statusText}`
        }
      } else if (err.request) {
        // Request was made but no response received
        errorMessage = 'Cannot connect to server. Please make sure the backend server is running on http://localhost:8000'
      } else if (err.message) {
        // Other error
        errorMessage = err.message
      }
      
      setError(errorMessage)
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
    <div className="vehicle-diagnostics">
      <header className="page-header">
        <button className="back-button" onClick={() => navigate('/')}>
          <FaArrowLeft /> Back to Dashboard
        </button>
        <h1>🚗 Vehicle Diagnostics</h1>
      </header>

      <main className="page-main">
        <div className="container">
          <div className="upload-section">
            <div
              {...getRootProps()}
              className={`dropzone ${isDragActive ? 'active' : ''} ${image ? 'has-image' : ''}`}
              data-tutorial="vehicle-upload"
            >
              <input {...getInputProps()} />
              {image ? (
                <div className="image-preview">
                  <img src={URL.createObjectURL(image)} alt="Preview" />
                  <p>{image.name}</p>
                  <button
                    className="remove-image"
                    onClick={(e) => {
                      e.stopPropagation()
                      setImage(null)
                    }}
                  >
                    Remove
                  </button>
                </div>
              ) : (
                <div className="dropzone-content">
                  <FaUpload size={48} />
                  <p>{isDragActive ? 'Drop the image here' : 'Drag & drop an image or click to select'}</p>
                  <p className="hint">Supports: PNG, JPG, JPEG</p>
                </div>
              )}
            </div>

            <div className="description-section" data-tutorial="vehicle-description">
              <label htmlFor="description">Additional Description (Optional)</label>
              <textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe the issue (e.g., 'Car won't start', 'Warning lights on dashboard')"
                rows={4}
              />
            </div>

            <button
              className="analyze-button"
              onClick={handleAnalyze}
              disabled={!image || loading}
              data-tutorial="vehicle-analyze"
            >
              {loading ? (
                <>
                  <FaSpinner className="spinner" /> Analyzing...
                </>
              ) : (
                'Analyze Vehicle'
              )}
            </button>
          </div>

          {error && (
            <div className="error-message">
              <FaExclamationTriangle /> {error}
            </div>
          )}

          {result && (
            <div ref={resultsRef} className="result-section" data-tutorial="vehicle-results">
              <h2>📊 Analysis Results</h2>

              <div className="result-card diagnosis">
                <h3>🔍 Diagnosis</h3>
                <p>{result.diagnosis}</p>
              </div>

              {result.recommended_actions && result.recommended_actions.length > 0 && (
                <div className="result-card actions">
                  <h3>📋 Recommended Actions</h3>
                  <ol>
                    {result.recommended_actions.map((action, index) => (
                      <li key={index}>{action}</li>
                    ))}
                  </ol>
                </div>
              )}

              {result.detailed_solution && result.detailed_solution.steps && result.detailed_solution.steps.length > 0 && (
                <div className="result-card solution">
                  <h3>🛠️ Detailed Solution</h3>
                  <ol>
                    {result.detailed_solution.steps.map((step, index) => (
                      <li key={index}>{step}</li>
                    ))}
                  </ol>
                </div>
              )}

              {result.emergency_contacts && result.emergency_contacts.length > 0 && (
                <div className="result-card contacts">
                  <h3>📞 Emergency Contacts</h3>
                  {result.emergency_contacts.map((contact, index) => (
                    <div key={index} className="contact-card">
                      <h4>{contact.name}</h4>
                      <p><FaPhone /> {contact.phone}</p>
                      {contact.website && <p>🌐 <a href={contact.website} target="_blank" rel="noopener noreferrer">{contact.website}</a></p>}
                      {contact.services && (
                        <p>Services: {contact.services.join(', ')}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}

export default VehicleDiagnostics
