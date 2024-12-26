import React from 'react';
import { createRoot } from 'react-dom/client';
import VolleyballSignup from './components/VolleyballSignup';
import './styles.css';

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('signup-root');
  
  if (!container) {
    console.error('Could not find signup-root element!');
    return;
  }

  try {
    const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <VolleyballSignup />
      </React.StrictMode>
    );
  } catch (error) {
    console.error('Error rendering React component:', error);
  }
});