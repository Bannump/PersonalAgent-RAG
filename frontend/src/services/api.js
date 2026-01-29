import axios from 'axios'

// Use relative URL to work with Vite proxy, or absolute if VITE_API_URL is set
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// #region agent log
fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:API_BASE_URL',message:'API base URL configured',data:{baseURL:API_BASE_URL,envVar:import.meta.env.VITE_API_URL},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
// #endregion

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 second timeout for image processing
})

export const vehicleDiagnostics = async (formData) => {
  // #region agent log
  fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:vehicleDiagnostics',message:'Vehicle diagnostics API call entry',data:{baseURL:API_BASE_URL,endpoint:'/vehicle',hasFormData:!!formData,formDataKeys:formData?Array.from(formData.keys()):[]},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
  // #endregion
  try {
    const response = await api.post('/vehicle', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 60000, // 60 second timeout for image processing
    })
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:vehicleDiagnostics',message:'Vehicle diagnostics API call succeeded',data:{status:response?.status,hasData:!!response?.data},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    return response.data
  } catch (error) {
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:vehicleDiagnostics',message:'Vehicle diagnostics API call failed',data:{errorType:error?.constructor?.name,errorMessage:error?.message,code:error?.code,hasRequest:!!error?.request,hasResponse:!!error?.response,status:error?.response?.status,statusText:error?.response?.statusText,responseData:error?.response?.data,baseURL:API_BASE_URL,fullURL:API_BASE_URL+'/vehicle'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
    // #endregion
    throw error
  }
}

export const resumeAnalysis = async (formData) => {
  // #region agent log
  fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:resumeAnalysis',message:'Resume analysis API call entry',data:{baseURL:API_BASE_URL,endpoint:'/resume/analyze',hasFormData:!!formData,formDataKeys:formData?Array.from(formData.keys()):[]},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
  // #endregion
  try {
    const response = await api.post('/resume/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:resumeAnalysis',message:'Resume analysis API call succeeded',data:{status:response?.status,hasData:!!response?.data},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    return response.data
  } catch (error) {
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:resumeAnalysis',message:'Resume analysis API call failed',data:{errorType:error?.constructor?.name,errorMessage:error?.message,code:error?.code,hasRequest:!!error?.request,hasResponse:!!error?.response,status:error?.response?.status,statusText:error?.response?.statusText,responseData:error?.response?.data,baseURL:API_BASE_URL,fullURL:API_BASE_URL+'/resume/analyze'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
    // #endregion
    throw error
  }
}

export const resumeBuilder = async (data) => {
  // #region agent log
  fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:resumeBuilder',message:'Resume builder API call entry',data:{baseURL:API_BASE_URL,endpoint:'/resume/build',hasData:!!data,dataKeys:data?Object.keys(data):[]},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'D'})}).catch(()=>{});
  // #endregion
  try {
    const response = await api.post('/resume/build', data)
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:resumeBuilder',message:'Resume builder API call succeeded',data:{status:response?.status,hasData:!!response?.data},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'A'})}).catch(()=>{});
    // #endregion
    return response.data
  } catch (error) {
    // #region agent log
    fetch('http://127.0.0.1:7244/ingest/0e1ab1fa-44ee-41aa-84fe-1dc40a600c3c',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({location:'api.js:resumeBuilder',message:'Resume builder API call failed',data:{errorType:error?.constructor?.name,errorMessage:error?.message,code:error?.code,hasRequest:!!error?.request,hasResponse:!!error?.response,status:error?.response?.status,statusText:error?.response?.statusText,responseData:error?.response?.data,baseURL:API_BASE_URL,fullURL:API_BASE_URL+'/resume/build'},timestamp:Date.now(),sessionId:'debug-session',runId:'run1',hypothesisId:'B'})}).catch(()=>{});
    // #endregion
    throw error
  }
}

export default api
