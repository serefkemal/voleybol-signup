import React from 'react';
import { createRoot } from 'react-dom/client';
import Login from './components/auth/Login';
import Signup from './components/auth/Signup';
import './styles.css';

document.addEventListener('DOMContentLoaded', () => {
  const loginRoot = document.getElementById('login-root');
  const signupRoot = document.getElementById('signup-root');

  if (loginRoot) {
    createRoot(loginRoot).render(<Login />);
  }
  if (signupRoot) {
    createRoot(signupRoot).render(<Signup />);
  }
});