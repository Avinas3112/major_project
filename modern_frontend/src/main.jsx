window.onerror = function (msg, url, lineNo, columnNo, error) {
  document.body.innerHTML += `<div style="color: red; padding: 20px; font-family: monospace;">
    <h3>Global JS Error</h3>
    <p>${msg}</p>
    <p>${url}:${lineNo}:${columnNo}</p>
    <pre>${error ? error.stack : ''}</pre>
  </div>`;
};

import React, { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  componentDidCatch(error, errorInfo) {
    console.error("React Error Caught:", error, errorInfo);
  }
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', color: 'red', fontFamily: 'sans-serif' }}>
          <h2>Something went wrong in the React rendering!</h2>
          <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#fee', padding: '10px' }}>
            {this.state.error && this.state.error.toString()}
            <br />
            {this.state.error && this.state.error.stack}
          </pre>
        </div>
      );
    }
    return this.props.children;
  }
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </StrictMode>,
)
