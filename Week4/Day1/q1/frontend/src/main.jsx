import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'  // Keep this for Tailwind
import './App.css'   // Custom styles for animations and enhancements
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
