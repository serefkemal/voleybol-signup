import React from 'react';
import { createRoot } from 'react-dom/client';
import GameDashboard from './components/admin/GameDashboard';
import './styles.css';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('game-dashboard-root');
  if (container) {
    const root = createRoot(container);
    root.render(<GameDashboard />);
  }
});