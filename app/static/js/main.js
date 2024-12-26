import React from 'react';
import { createRoot } from 'react-dom/client';
import Main from './components/Main';
import './styles.css';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('main-root');
  if (container) {
    const root = createRoot(container);
    root.render(<Main />);
  }
});