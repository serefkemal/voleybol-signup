import React from 'react';
import { createRoot } from 'react-dom/client';
import AdminLogin from './components/admin/AdminLogin';
import './styles.css';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('admin-root');
  if (container) {
    const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <AdminLogin />
      </React.StrictMode>
    );
  }
});