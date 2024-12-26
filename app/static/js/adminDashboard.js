import React from 'react';
import { createRoot } from 'react-dom/client';
import AdminDashboard from './components/admin/AdminDashboard';
import './styles.css';

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('admin-dashboard-root');
  if (container) {
    const root = createRoot(container);
    root.render(
      <React.StrictMode>
        <AdminDashboard />
      </React.StrictMode>
    );
  }
});