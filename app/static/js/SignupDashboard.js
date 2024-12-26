import React from 'react';
import { createRoot } from 'react-dom/client';
import SignupDashboard from './components/SignupDashboard';
import './styles.css';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('player-dashboard-root');
  if (container) {
    const root = createRoot(container);
    root.render(<SignupDashboard />);
  }
});