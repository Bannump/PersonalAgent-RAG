import axios from 'axios'

// Use VITE_API_URL for production, or /api for local development with proxy
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout for image processing
})

export const vehicleDiagnostics = async (formData) => {
  const response = await api.post('/vehicle', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 60000, // 60 second timeout for image processing
  })
  return response.data
}

export const resumeAnalysis = async (formData) => {
  const response = await api.post('/resume/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const resumeBuilder = async (data) => {
  const response = await api.post('/resume/build', data)
  return response.data
}

export default api
