import React from 'react';
import { createRoot } from 'react-dom/client';
import GameSignup from './components/GameSignup';
import './styles.css';

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('game-signup-root');
  
  if (!container) {
    console.error('Could not find game-signup-root element!');
    return;
  }

  try {
    const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <GameSignup />
      </React.StrictMode>
    );
  } catch (error) {
    console.error('Error rendering React component:', error);
  }
});