# My Personal Agent - Frontend Dashboard

React-based dashboard for My Personal Agent application with a dark theme.

## Features

- 🎨 Modern dark theme UI
- 🚗 Vehicle Diagnostics interface
- 📄 Resume Analysis & ATS Optimization
- 📝 Resume Builder
- ⚡ Fast and responsive
- 📱 Mobile-friendly

## Prerequisites

- Node.js 16+ and npm
- Backend API running (see main README.md)

## Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

## Development

```bash
# Start development server
npm run dev
```

The app will be available at `http://localhost:3000`

## Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Backend API

The frontend expects the backend API to be running at `http://localhost:8000/api`.

Update `src/services/api.js` or set `VITE_API_URL` environment variable to change the API URL.

## Environment Variables

Create a `.env` file in the frontend directory:

```env
VITE_API_URL=http://localhost:8000/api
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.jsx
│   │   ├── VehicleDiagnostics.jsx
│   │   ├── ResumeAnalysis.jsx
│   │   └── ResumeBuilder.jsx
│   ├── services/
│   │   └── api.js
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   └── index.css
├── public/
├── package.json
├── vite.config.js
└── README.md
```

## Technologies

- React 18
- React Router
- Axios
- React Dropzone
- React Icons
- Vite

## Notes

- The frontend is a separate React application
- Backend API endpoints need to be implemented (see backend documentation)
- All API calls are configured in `src/services/api.js`
